from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "tAt+DAXZ3oi7m/CG+LPZ/gRMFYK4buYUgMLhAy8mmbhbs1h0/9BQAboO2vZTh0hqxMJk+ZE5g6OMuVU3aJIQnd5PTe5dksefEblrys9+11L8XElGYw82enLdfJ/U6JCMovOziyAskZ/wAV+RDBxitQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "29a15a7ad0dc5797c2c42a33778184c2"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    print("📩 Body:", body)
    print("📩 Signature:", signature)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("⚠️ 署名エラー: チャネルシークレットが間違っているかも！")
        return 'Invalid signature', 403

    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()

    if user_msg.lower() == "/help":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="これはヘルプだよ！")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"あなたは「{user_msg}」と言いました。")
        )
