from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# 拡張機能側が credentials: 'include' で通信するため、supports_credentials=True が必須です
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return "Amazon Ranking API is running smoothly!"

# 💡 拡張機能（JS）が起動時に必ず通信してくる必須エンドポイント
@app.route('/api/get_current_usage', methods=['GET'])
def get_current_usage():
    try:
        # 本来はここでデータベース等と連携して残り回数を計算しますが、
        # まずはツールを最速で正常稼働させるために「無制限（プレミアム）」として返します。
        return jsonify({
            "is_premium": True,
            "remaining": 999
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
