import streamlit as st
import logging
from argument import create_argparser
import random
from model import chatgpt
import json
from prompt import *
import json
import re
with open('ClaimDecompose.json','r')  as f:
    data = json.load(f)

prompt_template = FactScore_PROMPT

def decouple_argument(claim):
    prompt = prompt_template.format(claim= claim)
    model_answer = chatgpt(prompt)
    sub_claims = model_answer.split('\n')

    return sub_claims
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

def validate_evidence(claim , evidence):
    claim = claim[:-1] if claim.endswith('.') else claim
    example = f"{evidence}\nBased on the above information, is it true that {claim}? True or False? The answer is: "
    answer_text = chatgpt(example)
    final_answer = map_direct_answer_to_label(answer_text)
    if final_answer == True:
        return '验证通过'
    else:
        return '验证失败'




def revise_argument(sub_claim, evidence):
    revise_prompt =  Revision_Prompt.format(claim = sub_claim, evidence = evidence)
    answer = chatgpt(revise_prompt)
    return f"修订后的分论点：{answer}（经过验证）"

if 'sub_arguments' not in st.session_state:
    st.session_state['sub_arguments'] = []
if 'selected_sub_arg' not in st.session_state:
    st.session_state['selected_sub_arg'] = ""
if 'evidence_text' not in st.session_state:
    st.session_state['evidence_text'] = ""
if 'validation_result' not in st.session_state:
    st.session_state['validation_result'] = ""
if 'revision_result' not in st.session_state:
    st.session_state['revision_result'] = ""


st.sidebar.title("功能菜单")
st.sidebar.markdown("### 使用说明")
st.sidebar.markdown("""
1. 输入复杂论点并点击“解耦”。
2. 选择分论点进行验证。
3. 输入证据并提交。
4. 验证通过后，可以进行修订。
""")

st.title("📝 论点解耦与验证工具")
st.markdown("---")  

input_claim = st.text_area("请输入复杂论点", height=150)

if st.button("解耦"):
    if input_claim:
     
        st.session_state['sub_arguments'] = [arg.strip('-') for arg in decouple_argument(input_claim) if arg.strip()]
        st.session_state['validation_result'] = ""  
        st.session_state['revision_result'] = ""    
        st.success("分论点已成功解耦！")  


if st.session_state['sub_arguments']:
    selected_arg = st.selectbox(
        "选择一个分论点进行验证", options=st.session_state['sub_arguments']
    )

    if selected_arg != st.session_state['selected_sub_arg']:
        st.session_state['selected_sub_arg'] = selected_arg
        st.session_state['evidence_text'] = ""
        st.session_state['validation_result'] = ""
        st.session_state['revision_result'] = ""


    st.session_state['evidence_text'] = st.text_area("请输入证据文本", value=st.session_state['evidence_text'], height=150)
    
    
    if st.button("提交证据"):
        
        st.write(f"您选择验证的分论点是：'{st.session_state['selected_sub_arg']}'")
        st.write(f"检索到的证据是：'{st.session_state['evidence_text']}'")
        st.session_state['validation_result'] = validate_evidence(st.session_state['selected_sub_arg'], st.session_state['evidence_text'])
        st.write(f"验证结果：{st.session_state['validation_result']}")


if st.session_state['validation_result'] == "验证通过":
    if st.button("修订"):
   
        st.session_state['revision_result'] = revise_argument(st.session_state['selected_sub_arg'],st.session_state['evidence_text'])
        
        st.success(st.session_state['revision_result'])  

