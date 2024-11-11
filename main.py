import logging
from argument import create_argparser
from tqdm import tqdm
from model import chatgpt
import json
from prompt import *

# 配置日志记录器
logging.basicConfig(filename='decompose.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(args):
    

        print(f'Precessing {args.datasets} dataset...')
        file_name  = f'{args.datasets}.json'
        with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
        
        prompt_template = globals().get(f'{args.baseline}_PROMPT')

    
        with open(f'{args.datasets}_{args.baseline}_{args.model}.json', 'a', encoding='utf-8') as file:
                for item in tqdm(range(len(data))):

                    #prompt = f'{args.baseline}_PROMPT'.format(claim = data[item]['claim'])
                    # 确保prompt_template不为空
                    if prompt_template:
                        prompt = prompt_template.format(claim=data[item]['claim'])
                    else:
                        print(f"Error: Prompt template for {args.baseline} not found.")
                    #print(prompt)
                    sub_claims = chatgpt(prompt)
                    data[item][f'{args.baseline}'] = sub_claims
                    # 记录日志
                    logger.info(f"Claim: {data[item]['claim']}, Result: {sub_claims}, Label: {data[item]['label']}")
                    #print(sub_claims)
                    file.write(json.dumps(data[item]))
                    file.write('\n')

if __name__ == '__main__':
    args = create_argparser()
    main(args)