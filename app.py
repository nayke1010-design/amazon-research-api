from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# 💡 重要：Amazonのページ（拡張機能）からの通信を許可する設定です
CORS(app, supports_credentials=True)

@app.route('/api/get_current_usage', methods=['GET'])
def get_usage():
    """
    拡張機能から「残り回数」や「プレミアム状態」を聞かれた時に答える場所です。
    現在はテスト用に『プレミアム会員』として返事をするようにしています。
    """
    return jsonify({
        "is_premium": True,   # プレミアム会員として判定
        "remaining": 999,       # 本日の残りリサーチ回数
        "usage_count": 0
    })

@app.route('/', methods=['GET'])
def index():
    return "Amazon Research API is running!"

if __name__ == "__main__":
    # 🚀 Renderなどのクラウドサーバーで動かすための専用設定です
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)