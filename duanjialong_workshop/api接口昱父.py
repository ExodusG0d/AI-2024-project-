from openai import OpenAI
from pathlib import Path

# 初始化OpenAI客户端
client = OpenAI(
    api_key="sk-S3mxoGD2VRIuKaisi5OEhEL3jPPTe8pHfEv0XHlzA0T2Rnnz",
    base_url="https://api.moonshot.cn/v1",  # 确保URL正确，去掉了错误的引号
)

def read_pdf(file_path):
    """使用Kimi API读取PDF文件内容"""
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    file_content = client.files.content(file_id=file_object.id).text
    return file_content

def chat(query, history):
    """实现聊天功能"""
    history.append({"role": "user", "content": query})
    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=history,
        temperature=0.3,
    )
    result = completion.choices[0].message.content
    history.append({"role": "assistant", "content": result})
    return result

# 初始化聊天历史
history = [
    {"role": "system", "content": "你是Kimi，由Moonshot AI提供的人工智能助手..."}
]

# 读取PDF文件内容
pdf_file_path = "C:/Users/Kevin Wu/Desktop/大三上/数据科学编程基础/html测试/“革命”是否“革官”_辛亥革命前后的县官人事变动_杜佩红 2(3).caj-2022-10-20-17-09-39-021.pdf"
pdf_content = read_pdf(pdf_file_path)

# 将PDF内容作为系统消息添加到历史记录中
history.append({"role": "system", "content": pdf_content})

# 现在可以基于PDF内容进行连续问答
print(chat("评价一下这份论文的内容要点", history))
print(chat("你觉得这个东西有前景吗？", history))
