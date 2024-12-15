from openai import OpenAI

def get_deepseek():
    client = OpenAI(api_key="", base_url="https://api.deepseek.com")
    return client

# response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=messages,
#         max_tokens=1024,
#         temperature=0.7,
#         stream=False
#     )
#     return   response.choices[0].message.content