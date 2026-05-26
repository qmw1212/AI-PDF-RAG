"""测试新版Gemini API并列出可用模型"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("错误：未找到GOOGLE_API_KEY")
    exit(1)

print(f"API密钥: {api_key[:10]}...")
print("\n正在初始化客户端...")

try:
    client = genai.Client(api_key=api_key)
    print("✓ 客户端初始化成功\n")

    # 尝试几个常见的模型名称
    test_models = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro',
        'models/gemini-pro',
    ]

    print("正在测试常见模型名称...")
    print("-" * 60)

    working_model = None

    for model_name in test_models:
        try:
            print(f"\n测试: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents="你好"
            )
            print(f"✓ 成功！模型 '{model_name}' 可用")
            print(f"  回答: {response.text[:50]}...")
            working_model = model_name
            break
        except Exception as e:
            error_str = str(e)
            if "404" in error_str or "NOT_FOUND" in error_str:
                print(f"✗ 模型不存在")
            else:
                print(f"✗ 错误: {error_str[:100]}")

    print("\n" + "-" * 60)

    if working_model:
        print(f"\n✓ 找到可用模型: {working_model}")
        print(f"\n请在 gemini_client.py 中使用: model='{working_model}'")
    else:
        print("\n⚠️ 未找到可用模型")
        print("\n可能的原因:")
        print("1. API密钥无效或已过期")
        print("2. API密钥没有访问Gemini模型的权限")
        print("3. 需要在Google AI Studio启用API访问")
        print("\n请访问: https://aistudio.google.com/app/apikey")

except Exception as e:
    print(f"\n✗ 初始化失败: {e}")

