from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# 💡 重要：Amazonのページ（拡張機能）やTampermonkeyからの通信を許可する設定です
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

# ====================================================
# 💡 【新規追加】ネットオフ専用の利益判定API（B部署）
# ====================================================
@app.route('/api/netoff/profit', methods=['GET'])
def netoff_profit():
    # Tampermonkeyから「ISBN」と「ネットオフの仕入値」を受け取る
    isbn = request.args.get('isbn')
    buy_price = request.args.get('buy_price', type=int)

    if not isbn or buy_price is None:
         return jsonify({"status": "error", "message": "データ不足"}), 400

    try:
        # 🚨 本来はここでAmazon SP-APIを使って実際の価格を取得しますが、
        # まだSP-APIの処理が作られていないため、今回は「テスト用のダミー計算」を行います。
        # （仕入値 ＋ 2000円 でAmazonで売られていると仮定します）
        amazon_price = buy_price + 2000 
        
        # 利益計算（例：手数料を仮に15%とした場合）
        fee = int(amazon_price * 0.15)
        profit = amazon_price - buy_price - fee

        # 利益が500円以上なら「合格（is_target: true）」とする
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
    # 🚀 Renderなどのクラウドサーバーで動かすための専用設定です
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
