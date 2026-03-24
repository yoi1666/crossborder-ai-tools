from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    keywords = data.get('keywords')
    platform = data.get('platform')
    
    if platform == 'amazon':
        prompt = f"作为亚马逊Listing优化专家，为产品关键词'{keywords}'生成：1. 标题（含5个核心关键词）2. 五点描述（每个点突出一个卖点，含emoji）3. 产品描述（200字，包含关键词）"
    else:
        prompt = f"作为Shopify营销专家，为产品关键词'{keywords}'生成：1. 产品标题（吸引眼球）2. 卖点列表（含图标）3. 产品描述（故事化，200字）"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
    result = response.json()
    content = result['choices'][0]['message']['content']
    
    return jsonify({"content": content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
