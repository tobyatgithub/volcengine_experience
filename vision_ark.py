import base64
import os

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 通过 pip install volcengine-python-sdk[ark] 安装方舟SDK
from volcenginesdkarkruntime import Ark

# 替换 <Model> 为模型的Model ID
model = "doubao-1.5-vision-pro-32k-250115"

# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    api_key=os.getenv("api-key-20250305161245-wework"),
)


# 定义方法将指定路径图片转为Base64编码
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image("./images/1742216223472.jpg")
# 创建一个对话请求
response = client.chat.completions.create(
    # 指定您部署了视觉理解大模型的推理接入点ID
    model=model,
    messages=[
        {
            # 指定消息的角色为用户
            "role": "user",
            "content": [
                # 文本消息，希望模型根据图片信息回答的问题
                {
                    "type": "text",
                    "text": "图中是一个学生写的英语作业。请你识别一下图中的文字，并按照其结构打印出来。注意一定要包含原来的题目，加上学生手写的作答。",
                },
                # 图片信息，希望模型理解的图片
                {
                    "type": "image_url",
                    "image_url": {
                        # "url": "https://github.com/tobyatgithub/volcengine_experience/blob/main/images/1742216223472.jpg?raw=true"
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ],
)

print(response.choices[0].message.content)
