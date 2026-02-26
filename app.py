from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# 全ドメインからのアクセスを許可（テスト用）
CORS(app)

@app.route('/')
def index():
    return "Amazon Research API is running!"

@app.route('/api/get_current_usage', methods=['GET'])
def get_usage():
    return jsonify({
        "is_premium": True,
        "remaining": 999,
        "usage_count": 0
    })

# 💡 ネットオフ・駿河屋共通の利益判定窓口
@app.route('/api/netoff/profit', methods=['GET'])
def netoff_profit():
    isbn = request.args.get('isbn')
    buy_price = request.args.get('buy_price', type=int)

    if not isbn or buy_price is None:
         return jsonify({"status": "error", "message": "Missing Data"}), 400

    try:
        # 現在はテスト用のダミー計算（後にSP-APIへ差し替え）
        amazon_price = buy_price + 2000 
        fee = int(amazon_price * 0.15)
        profit = amazon_price - buy_price - fee
        is_target = profit >= 500

        return jsonify({
            "status": "success",
            "is_target": is_target,
            "profit": profit,
            "amazon_price": amazon_price,
            "buy_price": buy_price
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Renderの環境変数 PORT を読み込む
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
