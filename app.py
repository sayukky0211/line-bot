from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os
import time

app = Flask(__name__)

# 環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
openai.api_key = OPENAI_API_KEY

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    # メンションされたか確認（@が含まれるなどの単純な例）
    if '@' in text or 'bot' in text.lower():
        reply_text = generate_chatgpt_response(text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

def generate_chatgpt_response(user_text):
    try:
        start = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは明るくてかわいい女の子のようにふるまうAIです。丁寧だけどフレンドリーに答えてね！"},
                {"role": "user", "content": user_text}
            ]
        )
        duration = round((time.time() - start) * 1000)
        reply = response['choices'][0]['message']['content']
        return f"{reply}\n（処理時間: {duration}ms）"
    except Exception as e:
        return f"ごめんね、ちょっとエラーが出ちゃったみたい……！\n{e}"

if __name__ == "__main__":
    app.run()
