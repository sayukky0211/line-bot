from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境変数からチャネルシークレットとアクセストークンを取得
LINE_CHANNEL_ACCESS_TOKEN = "tAt+DAXZ3oi7m/CG+LPZ/gRMFYK4buYUgMLhAy8mmbhbs1h0/9BQAboO2vZTh0hqxMJk+ZE5g6OMuVU3aJIQnd5PTe5dksefEblrys9+11L8XElGYw82enLdfJ/U6JCMovOziyAskZ/wAV+RDBxitQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "29a15a7ad0dc5797c2c42a33778184c2"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
    handler.handle(body, signature)
except InvalidSignatureError:
    # abort(400)
    print("⚠️ Invalid signature!")
    return 'Invalid signature'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()

    if user_msg.lower() == "/help":
        help_text = (
            "📌 **使えるコマンド一覧**\n\n"
            "・/help - このヘルプを表示\n"
            "・/ping - 応答確認\n"
            "・/say <メッセージ> - Botが繰り返す（管理者限定）\n"
            "・@Bot名 <メッセージ> - メンションに応答\n"
            "・画像生成・翻訳・天気・検索なども順次追加予定！"
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=help_text)
        )
    else:
        # デフォルトの反応
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"「{user_msg}」って言ったね！\n→ /help でコマンド確認できるよ✨")
        )
