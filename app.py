from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # 外部（ブラウザ）からの通信を許可

@app.route('/')
def index():
    return "Amazon Research API is running!"

@app.route('/api/profit', methods=['GET'])
def calculate_profit():
    isbn = request.args.get('isbn')
    buy_price = request.args.get('buy_price', type=int)

    if not isbn or buy_price is None:
         return jsonify({"status": "error", "message": "Data Missing"}), 400

    try:
        # 【テスト用】現在は一律で「仕入値 ＋ 2000円」をAmazon合計価格と仮定
        amazon_total_price = buy_price + 2000 

        # 💡 教えていただいた計算式を正確に反映
        # 利益 $X = (Amazon合計 \times 0.85) - 155 - 仕入れ価格$
        profit = int((amazon_total_price * 0.85) - 155 - buy_price)

        # 💡 テスト用：利益が1円以上なら「お宝」判定（is_target: true）
        is_target = profit >= 1

        return jsonify({
            "status": "success",
            "is_target": is_target,
            "profit": profit,
            "amazon_total": amazon_total_price,
            "buy_price": buy_price
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
