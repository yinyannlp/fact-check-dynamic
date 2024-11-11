from openai import OpenAI,OpenAIError


# 设置 API key 和 API base URL
api_key = ""
open_key = ""
base_url = "https://api.132999.xyz/v1"
import requests
import time

def chatgptv2(text):
    api_url = 'https://api.132999.xyz/v1/chat/completions'


    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}
    request_data = {
        
        'messages': [
            {'role': 'system', 'content': 'You are ChatGPT, a large language model trained by OpenAI.'},
            {'role': 'user', 'content': text}
        ],
        'stream': False,
        'model': 'gpt-3.5-turbo-1106',
        'temperature': 0.1,
        'presence_penalty': 0,
        'frequency_penalty': 0,
        'top_p': 0.75
    }

    response = requests.post(api_url, headers=headers, json=request_data)
    data = response.json()
    return data['choices'][0]['message']['content']


def chatgpt(text):
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    for attempt in range(3):  # 尝试3次
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
                model="gpt-3.5-turbo-1106",
            )
            return chat_completion.choices[0].message.content
        except OpenAIError as e:
            print(f"Request failed: {e}")
            if attempt < 2:  # 只在不是最后一次尝试时等待
                print("Retrying in 5 seconds...")
                time.sleep(5)  # 等待5秒后重新尝试
            else:
                print("Max retries reached. Exiting.")
                raise

