import requests
from tqdm import tqdm 
import json
import re
import pdb
import os
from argument import create_argparser
import warnings
import logging
from model import chatgpt,chatgptv2
import random

logging.basicConfig(filename='verify.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_question_command(command, variable_map):
    return_var, tmp = command.split('= Question')
    return_var = return_var.strip()
    # question = tmp.replace("\")", "").strip()

    p1 = re.compile(f'Question\([f]?\"(.*)\"\)', re.S)
    matching = re.findall(p1, command)
    question = matching[0] if len(matching)>0 else tmp

    # replace variable
    #pdb.set_trace()
    for variable_name, variable_value in variable_map.items():
        replace_var = "<" + str(variable_name) + ">"
        if question.find(replace_var) >=0:
            question = question.replace(replace_var, variable_value)
    # Add return_var to variable_map with value set to None
    #pdb.set_trace()
    variable_map[return_var] = None
    return return_var, question


def parse_verify_command(command, variable_map):
    return_var, tmp = command.split('= Verify')
    return_var = return_var.strip()
    # claim = tmp.replace("\")", "").strip()

    p1 = re.compile(f'Verify\([f]?\"(.*)\"\)', re.S)
    matching = re.findall(p1, command)
    claim = matching[0] if len(matching)>0 else tmp

    # replace variable
    for variable_name, variable_value in variable_map.items():
        replace_var = "<" + str(variable_name) + ">"
        variable_value = str(variable_value)
        if claim.find(replace_var) >=0:
            claim = claim.replace(replace_var, variable_value)
            # pdb.set_trace()
            print("Replace :",claim)
            # pdb.set_trace()
    
    return return_var, claim

def answer_verify_question(claim , evidence ):
    claim = claim[:-1] if claim.endswith('.') else claim
    example = f"{evidence}\nBased on the above information, is it true that {claim}? True or False? The answer is: "
    answer_text = chatgpt(example)

    return answer_text

def answer_question_directly(question, evidence,model):
    
    example = f"{evidence}\nQuestion: {question}\nThe answer is:"

   
    answer_text = chatgpt(example
        )
    
    
    return answer_text

def answer_program(program,evidence):   
    variable_map = {}
    for command in program:
        c_type = get_command_type(command)
        final_answer = True
       
        # 验证声明
        if c_type == "VERIFY":
                try:
                    return_var, claim = parse_verify_command(command,variable_map)
                    claim =  re.sub('</s>', '', claim)
                    return_var = return_var.strip()
                    answer = answer_verify_question(claim, evidence)
                    variable_map[return_var] = map_direct_answer_to_label(answer)
                except:
                    final_answer = random.sample([True, False], 1)[0]
     # 提问命令
        elif c_type == "QUESTION":
            try:
                return_var, question = parse_question_command(command, variable_map)
                answer = answer_question_directly(question, evidence)
                variable_map[return_var] = answer
            except:
                final_answer = random.sample([True, False], 1)[0]
    try:        
        pattern = r"fact_\d+"
        values = [value for key, value in variable_map.items() if re.search(pattern, key)]
        final_answer = all(values)
    except:
        print(f"Alert!!! parsing error")
        final_answer = random.sample([True, False], 1)[0]
        
    return final_answer,variable_map
           

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
        return False


                
          
def derive_final_answer(command, variable_map):
        final_label = True
        command = command.replace('label =', '').strip()
        p1 = re.compile(r'Predict[(](.*?)[)]', re.S)
        command_arg = re.findall(p1, command)[0]
        verify_subs = command_arg.split(" and ")
        arguments = [arg.strip() for arg in verify_subs]
      
        for argument in arguments:
            if argument in variable_map:
                final_label = variable_map[argument] and final_label
            else:
                print(f"Alert!!! wrong argument: {argument}")
            
        return final_label
    

def split_claim(text):
  
    match = re.search(r'^([^=:]+)(=|:)', text)
    if not match:
        return None, None
    first_part = match.group(1).strip()
    separator = match.group(2)
    second_part = text[match.end():].strip()
    claim_match = re.search(r'claim\D*(\d+)', first_part)   
    if claim_match:     
        num = claim_match.group(1)  
        return f'sub-claim_{num}', second_part
    else:
        return None, None




def get_command_type(command):
    if command.find("label = ")>=0:
        return "FINAL"
    elif command.find('= Verify')>=0:
        return "VERIFY"
    elif command.find('= Question')>=0:
        return "QUESTION"
    elif command.find('= Relation')>=0:
        return "RELATION"
    else:
        return "UNKNOWN"


def get_f1(data,method):
    labels = []
    predict = []
    for item in range(len(data)):
            labels.append(data[item]['label'])
            predict.append(data[item][f'{method}_label'])
    map = {'Supported':True,'supports':True,'true':True ,'SUPPORTED':True,'entailment':True,'mostly-true':True,'yes':True,True : True,False:False,'yes':True,'SUPPORTS':True}
    # 使用列表推导式应用映射
    original_labels = [map.get(item, False) for item in labels]
    predict_labels = [map.get(item, False) for item in predict]
    from sklearn.metrics import f1_score
    # 计算F1指标n
    f1 = f1_score(original_labels, predict_labels,average='macro')

    return f1

def main(args):
    data = []
    with open(f'{args.datasets}_{args.baseline}_{args.model}.json','r',encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    
        print(f"Now {args.datasets}_{args.baseline}_{args.model} Answer Program !!!!!!")
    with open(f'{args.datasets}_{args.baseline}_{args.model}_verify.json','a') as f:
                    for item in tqdm(range(len(data))):
                        evidence = ''
                        if isinstance(data[item]['evidence'],str):
                                evidence = data[item]['evidence']
                        else:
                            for i in data[item]['evidence']:
                                evidence = evidence + i
                        verify_program = data[item][f'{args.baseline}'].split('\n')
                        try:
                             
                            if args.baseline == 'ProgramFC':
                                predict_result, _ = answer_program(verify_program,evidence)
                                data[item][f'{args.baseline}_label'] = predict_result
                    
                            if args.baseline == 'Wice' or args.baseline == 'FactScore':
                                final_answer = True
                                for text in verify_program:
                                    sub_claim = re.sub(r'^-[\s]*', '', text)
                                    raw_answer = answer_verify_question(sub_claim,evidence)
                                    answer = map_direct_answer_to_label(raw_answer)
                                    final_answer = final_answer and answer
                                data[item][f'{args.baseline}_label'] = final_answer
                            if args.baseline == 'Coling':
                                 # 正则表达式，直接匹配 Sub-claim_x 冒号后的文本
                                pattern = r'Sub-claim_\d\s*:\s*(.+)'

                                # 遍历列表，提取符合条件的文本
                                extracted_claims = [re.search(pattern, text).group(1) for text in verify_program if re.search(pattern, text)]
                                final_answer = True
                                # 输出提取的结果
                                for i, sub_claim in enumerate(extracted_claims, 1):
                                    raw_answer =   answer_verify_question(sub_claim,evidence)
                                    answer = map_direct_answer_to_label(raw_answer)
                                    final_answer = final_answer and answer
                                data[item][f'{args.baseline}_label'] = final_answer
                        except:
                            data[item][f'{args.baseline}_label'] = random.sample([True, False], 1)[0]
                        f.write(json.dumps(data[item]))
                        f.write('\n')
                    f1 = get_f1(data,args.baseline)
                    print(f"{args.datasets}_{args.baseline}_{args.model}_f1 result :",f1)
                    logger.info(f'Dataset: {args.datasets},Baseline : {args.baseline},f1: {f1}')
                    
                       
                
if __name__ == '__main__':
    args = create_argparser()
    main(args)
