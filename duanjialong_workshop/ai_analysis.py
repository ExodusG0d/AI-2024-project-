import mimetypes
import logging
from openai import OpenAI
from pathlib import Path

# 初始化OpenAI客户端
client = OpenAI(
    api_key="sk-S3mxoGD2VRIuKaisi5OEhEL3jPPTe8pHfEv0XHlzA0T2Rnnz",
    base_url="https://api.moonshot.cn/v1",  # 确保URL正确，去掉了错误的引号
)


def read_pdf(file_path):
        file_object = client.files.create(file=Path(file_path), purpose="file-extract")
        file_content = client.files.content(file_id=file_object.id).text
        return file_content


def chat(query, history):
    try:
        # 添加用户问题到聊天历史
        history.append({"role": "user", "content": query})

        # 调用 Kimi API 生成回答
        completion = client.chat.completions.create(
            model="moonshot-v1-128k",  # 指定模型
            messages=history,
            temperature=0.3,  # 调节回答的随机性
        )

        # 获取回答内容
        result = completion.choices[0].message.content

        # 添加 AI 回答到聊天历史
        history.append({"role": "assistant", "content": result})
        return result
    except Exception as e:
        raise RuntimeError(f"聊天功能调用失败: {str(e)}")


def run_analysis(file_path):
    try:
        print("Running analysis...")

        # 初始化聊天历史
        history = [
            {"role": "system", "content": "你是Kimi，由Moonshot AI提供的人工智能助手..."}
        ]

        # 提取 PDF 内容
        pdf_content = read_pdf(file_path)

        # 将 PDF 内容作为系统消息添加到历史记录
        history.append({"role": "system", "content": pdf_content})

        # 提出问题并获取回答
        summary = chat("请提供这篇论文的摘要", history)
        methodology = chat("请描述这篇论文的研究方法", history)
        conclusion = chat("请总结这篇论文的结论", history)
        recommendations = chat("请推荐一些相关的论文", history)

        return {
            "summary": summary,
            "methodology": methodology,
            "conclusion": conclusion,
            "recommendations": recommendations,
            "message": "Analysis complete!"
        }
    except ValueError as e:
        return {"error": f"分析失败: {str(e)}"}
    except Exception as e:
        return {"error": f"分析失败: {str(e)}"}

