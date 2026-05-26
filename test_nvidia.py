"""测试NVIDIA API"""
from openai import OpenAI

api_key = "***REMOVED***"

print("正在测试NVIDIA API...")
print(f"API密钥: {api_key[:20]}...")

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1"
    )

    print("\n✓ 客户端初始化成功")
    print("\n正在列出可用模型...")
    print("-" * 60)

    # 列出可用模型
    models = client.models.list()

    print(f"\n找到 {len(models.data)} 个可用模型：\n")

    for model in models.data[:10]:  # 只显示前10个
        print(f"  • {model.id}")

    if len(models.data) > 10:
        print(f"\n  ... 还有 {len(models.data) - 10} 个模型")

    print("\n" + "-" * 60)

    # 测试一个常用模型
    test_models = [
        "meta/llama-3.1-8b-instruct",
        "nvidia/llama-3.1-nemotron-70b-instruct",
        "mistralai/mixtral-8x7b-instruct-v0.1"
    ]

    print("\n正在测试模型...")
    working_model = None

    for model_name in test_models:
        try:
            print(f"\n测试: {model_name}")
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "你好，请用一句话介绍自己"}],
                max_tokens=100
            )
            print(f"✓ 成功！")
            print(f"  回答: {response.choices[0].message.content[:80]}...")
            working_model = model_name
            break
        except Exception as e:
            error_str = str(e)
            if "not found" in error_str.lower() or "404" in error_str:
                print(f"✗ 模型不可用")
            else:
                print(f"✗ 错误: {error_str[:100]}")

    print("\n" + "-" * 60)

    if working_model:
        print(f"\n✓ NVIDIA API可用！")
        print(f"✓ 推荐使用模型: {working_model}")
    else:
        print("\n⚠️ 需要手动选择可用模型")
        print("请从上面的模型列表中选择一个")

except Exception as e:
    print(f"\n✗ 测试失败: {e}")
    print("\n可能的原因:")
    print("1. API密钥无效")
    print("2. 网络连接问题")
    print("3. API额度不足")
