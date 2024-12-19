#pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple 下载国内镜像网站
from openai import OpenAI

client = OpenAI(
    api_key="sk-xoF2WpsdA7Fk8c1cyZg0PvlpEBmxydRsltg3Pn6Z7dQog6gI",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
    ],
    temperature=0.3,
)

# 通过 API 我们获得了 Kimi 大模型给予我们的回复消息（role=assistant）
print(completion.choices[0].message.content)

#pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple 下载国内镜像网站
from openai import OpenAI

client = OpenAI(
    api_key="sk-xoF2WpsdA7Fk8c1cyZg0PvlpEBmxydRsltg3Pn6Z7dQog6gI",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
    ],
    temperature=0.3,
)

# 通过 API 我们获得了 Kimi 大模型给予我们的回复消息（role=assistant）
print(completion.choices[0].message.content)

#%%
from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="MOONSHOT_API_KEY"  # 替换为你从 Kimi 开放平台申请的 API Key
)

# 定义全局变量 messages
messages = [
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
]

# 定义聊天函数
def chat(input: str) -> str:
    """
    chat 函数支持多轮对话，每次调用 chat 函数与 Kimi 大模型对话时，Kimi 大模型都会”看到“此前已经
    产生的历史对话消息，换句话说，Kimi 大模型拥有了记忆。
    """
    global messages  # 声明全局变量

    # 添加用户消息到 messages
    messages.append({
        "role": "user",
        "content": input
    })

    # 调用 API，生成对话结果
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
        temperature=0.3
    )

    # 获取助手回复
    assistant_message = completion.choices[0].message

    # 将助手的回复添加到 messages
    messages.append(assistant_message)

    return assistant_message.content

# 测试对话


def nb(x):
    return x+1