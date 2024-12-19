import os
import tempfile
from flask import Flask, render_template, jsonify, request
from ai_analysis import run_analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/chat-analysis')
def chat_analysis():
    return render_template('chat_analysis.html')

@app.route('/run_analysis', methods=['POST'])
def run_analysis_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # 保存上传的文件到临时目录
    temp_file_path = os.path.join('/tmp', uploaded_file.filename)
    uploaded_file.save(temp_file_path)

    # 调用分析函数
    result = run_analysis(temp_file_path)

    # 删除临时文件
    os.remove(temp_file_path)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

