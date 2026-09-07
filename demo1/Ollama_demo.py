from ollama import Client

# 指向局域网ollama机器
client = Client(host="http://127.0.0.1:11434")

# 全局保存对话上下文
messages = []

def chat_with_ollama(user_input: str) -> str:
    """封装原有循环里的对话逻辑，给外部调用"""
    global messages
    if user_input.strip() == "":
        return ""
    # 把规则写在这里，每次请求带上
    system_rule = """
你是一名专业助手。
规则：
1. 不要输出思考过程，直接输出最终回答；
2. 回答简洁精炼，分点输出；
3. 如果是代码，只输出可运行代码，不要多余解释；
4. 每次回答都要在结尾加上ok。
"""
    full_prompt = f"{system_rule}\n用户问题：{user_input}"
    messages.append({"role": "user", "content": full_prompt})

    response = client.chat(
        model="deepseek-r1:1.5b", 
        messages=messages
    )
    ai_reply = response.message.content
    messages.append({"role": "assistant", "content": ai_reply})
    return ai_reply

# 保留原来控制台循环交互，直接运行这个文件还可以终端对话
if __name__ == "__main__":
    while True:
        user_input = input("你：")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        res = chat_with_ollama(user_input)
        print(f"AI：{res}")
