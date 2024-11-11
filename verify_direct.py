import json
import sklearn
from argument import create_argparser
from model import chatgpt
import re,random
from tqdm import tqdm
def answer_verify_question(claim , evidence ):
    claim = claim[:-1] if claim.endswith('.') else claim
    example = f"{evidence}\nBased on the above information, is it true that {claim}? True or False? The answer is: "
    answer_text = chatgpt(example)
    #print(answer_text)
    return answer_text

def map_direct_answer_to_label(predict):
    predict = predict.lower().strip()  
    predict = re.sub(r'[^\w\s]', ' ', predict)  
    label_map = {
        'true': True,
        'false': False,
        'yes': True,
        'no': False,
        "it's impossible to say": False,
        'the given information does not': False,
        'not':False,
        'unkown':False,
        'it is impossible to':False,
        'it is not explicitly':False,
        'don`t':False,
        'doesn`t':False
    }
    found_key = None
    for key in label_map.keys():
        if re.search(r'\b' + key + r'\b', predict):
            found_key = key
            break
    

    if found_key:
        return label_map[found_key]
    else:
        print(f"Alert!!! wrong answer mapping: {predict}")
        return random.choice([True, False])
    
def get_f1(data,method):
    labels = []
    predict = []
    for item in range(len(data)):
        

        labels.append(data[item]['label'])
        predict.append(data[item][f'{method}_label'])
        
    map = {'Supported':True,'entailment':True,'SUPPORTED':True,'supports':True,'true':True ,'mostly-true':True,'yes':True,True : True,False:False,'yes':True,'SUPPORTS':True}
    # 使用列表推导式应用映射
    original_labels = [map.get(item, False) for item in labels]
    predict_labels = [map.get(item, False) for item in predict]
    from sklearn.metrics import f1_score
    # 计算F1指标n
    f1 = f1_score(original_labels, predict_labels,average='macro')

    return f1

def main(args):
   
    data = []
    with open(f'{args.datasets}.json','r',encoding='utf-8') as f:
        data = json.load(f)
    
        print(f"Now {args.datasets}_{args.baseline}_{args.model} Answer Program !!!!!!")
    with open(f'{args.datasets}_{args.baseline}_{args.model}_verify.json','a') as f:
        for item in tqdm(range(len(data))):
            try:
                if isinstance(data[item]['evidence'],str):

                    raw_result = answer_verify_question(data[item]['claim'],data[item]['evidence'])
                   
                else:
                    evidence = ''
                    for i in data[item]['evidence']:
                        evidence = evidence + i 
                    raw_result = answer_verify_question(data[item]['claim'],evidence)
                result = map_direct_answer_to_label(raw_result)
                data[item][f'{args.baseline}_label'] = result
            except:
                data[item][f'{args.baseline}_label'] = random.choice([True, False])
            f.write(json.dumps(data[item]))
            f.write('\n')
        f1 = get_f1(data,args.baseline)
        print(f'{args.datasets}_{args.baseline}_{args.model}_f1 : ' ,f1)
if __name__ == '__main__':
    args = create_argparser()
    main(args)