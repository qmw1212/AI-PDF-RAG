"""AI API调用模块 - 支持NVIDIA和DeepSeek"""
import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    """保持类名不变，避免修改app.py"""
    def __init__(self):
        # 优先使用NVIDIA API，如果没有则使用DeepSeek
        nvidia_key = os.getenv("NVIDIA_API_KEY")
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")

        if nvidia_key:
            print("[INFO] 使用NVIDIA API")
            self.client = OpenAI(
                api_key=nvidia_key,
                base_url="https://integrate.api.nvidia.com/v1"
            )
            self.model = "meta/llama-3.1-8b-instruct"
            self.provider = "NVIDIA"
        elif deepseek_key:
            print("[INFO] 使用DeepSeek API")
            self.client = OpenAI(
                api_key=deepseek_key,
                base_url="https://api.deepseek.com"
            )
            self.model = "deepseek-chat"
            self.provider = "DeepSeek"
        else:
            raise ValueError("请在.env文件中设置NVIDIA_API_KEY或DEEPSEEK_API_KEY")

    def generate_answer(self, question: str, context: List[str]) -> str:
        """基于检索到的上下文生成答案"""
        import time
        print(f"[DEBUG] 开始生成答案，时间: {time.strftime('%H:%M:%S')}")
        print(f"[DEBUG] 使用: {self.provider} - {self.model}")
        print(f"[DEBUG] 问题: {question}")
        print(f"[DEBUG] 上下文块数: {len(context)}")

        context_text = "\n\n".join(context)

        prompt = f"""基于以下上下文回答问题。如果上下文中没有相关信息，请说明无法从提供的文档中找到答案。

上下文：
{context_text}

问题：{question}

回答："""

        try:
            print(f"[DEBUG] 正在调用{self.provider} API...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文档问答助手，请根据提供的上下文准确回答用户的问题。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048,
                timeout=30
            )

            print(f"[DEBUG] API调用成功，时间: {time.strftime('%H:%M:%S')}")
            return response.choices[0].message.content

        except Exception as e:
            error_msg = str(e)
            print(f"[DEBUG] API调用失败: {error_msg}")

            # 提供更友好的错误信息
            if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                return "⚠️ 连接超时：请检查网络连接"
            elif "api key" in error_msg.lower() or "api_key" in error_msg.lower() or "unauthorized" in error_msg.lower():
                return f"⚠️ API密钥错误：请检查.env文件中的{self.provider}_API_KEY是否正确"
            elif "insufficient" in error_msg.lower() or "quota" in error_msg.lower():
                return f"⚠️ API额度不足：请前往{self.provider}平台充值"
            else:
                return f"生成答案时出错：{error_msg}"
