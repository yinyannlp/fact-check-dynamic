import requests
from tqdm import tqdm 
import json
import re
import pdb
import os

import warnings
import logging
logging.basicConfig(level=logging.ERROR)
import random
from openai import OpenAI
api_key = ""
open_key = ""
base_url = "https://api.132999.xyz/v1"

client = OpenAI(
    api_key=api_key,
    base_url = base_url
)

import openai

# 使用 %env 设置的环境变量
def gpt4(prompt):
  response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  messages=[
    {
      "role": "user",
      "content": prompt
    }
  ]
)
  return response.choices[0].message.content






def answer_verify_question(claim , evidence , model):
    claim = claim[:-1] if claim.endswith('.') else claim
    example = f"{evidence}\nBased on the above information, is it true that {claim}? True or False? The answer is: "
    answer_text = gpt4(example)
    #print(answer_text)
    return answer_text

def answer_program(claim,evidence,model):   
    #variable_map = {}
    #for command in program:
        #c_type = get_command_type(command)
    final_answer = None
        #print(c_type)
        # 验证声明
        #if c_type == "VERIFY":
    #try:
        #claim = command
       # claim =  re.sub('</s>', '', claim)
        #print(return_var, claim)
        #return_var = return_var.strip()
        #pdb.set_trace()
        #if len(evidence.split()) > 1536:
        #   print('evidence is too long, cut it to max_evidence_length')
        #  evidence = ' '.join(evidence.split()[:1536])
      
           
    answer = answer_verify_question(claim, evidence,model)

            #variable_map[return_var] = answer

    final_answer = map_direct_answer_to_label(answer)
        

        
                
                
    
   
    return final_answer
        

    
    
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

def get_f1(data,dataset,answer_model):
    labels = []
    predict = []
    for item in range(len(data)):
        if 'label' in data[item].keys():

            labels.append(data[item]['label'])
            predict.append(data[item][f'{dataset}_{answer_model}_result'])
        else:
            labels.append(data[item]['annotated_label'])
            predict.append(data[item][f'{dataset}_{answer_model}_result'])
    map = {'Supported':True,'entailment':True,'supports':True,'true':True ,'mostly-true':True,'yes':True,True : True,False:False,'yes':True}
    # 使用列表推导式应用映射
    original_labels = [map.get(item, False) for item in labels]
    predict_labels = [map.get(item, False) for item in predict]
    from sklearn.metrics import f1_score
    # 计算F1指标n
    f1 = f1_score(original_labels, predict_labels,average='binary')

    return f1

def get_command_type(command):  
    if 'claim' in command:
        return "VERIFY"
    else:
        return None  


generate_models = ['llama7b','llama13b','llama72b']
answer_models = ['gpt_3.5']
datasets = ['Wice']
count = 0
for dataset in datasets:
    data = []
    with open('/Users/lingxiao/Nutstore Files/我的坚果云/dataset/Wice.json','r') as f:
        for line in f:
            data.append(json.loads(line))
    for answer_model in answer_models:
                
        print(f"Now {answer_model} Answer Program !!!!!!")
        with open(f'{dataset}_{answer_model}_200.json','a') as f:
            for item in tqdm(range(len(data))):
                
                    try:
                        result = answer_program(data[item]['claim'], data[item]['evidence'],answer_model)
                        if result == False:
                            data[item][f'{dataset}_{answer_model}_result'] = False
                        else:
                            data[item][f'{dataset}_{answer_model}_result'] = result
                    except:
                        result = random.choice([True, False])
                    if result == True:
                        count = count + 1
                    #data[item][f'{dataset}_{answer_model}_decpompose_map'] = temp_map
                    #print(data[item]['label'])
                    #print(f'{dataset}_{answer_model}_result:', result)
                    f.write(json.dumps(data[item]))
                    f.write("\n")  
            print("acc is ", count/len(data))
        f1 = get_f1(data,dataset,answer_model)
   
        with open('all_gpt_result0607.txt','a') as f:
            
            f.write(f"{dataset}_{answer_model}_result : {f1}\n")
            print(f"{dataset}_{answer_model}_result : {f1}\n")
       

                    
