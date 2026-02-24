
import os
# 调用通义大模型
from langchain_community.llms.tongyi import Tongyi


model = Tongyi(
    model = "qwen-max",
    api_key = os.getenv("DASHSCOPE_API_KEY")
)

print(model.invoke("你是谁"))