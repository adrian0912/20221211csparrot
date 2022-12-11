from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('XwZQ5Lpfz1FZSy//4pysXPzH5ajedewp6Smrntr1vqgDZWaWTfgglXZy/xhhEBSA6YFM9VwLtxDW5r10w66KxEvyBys7Et2bjdOrMWks27OYTyve/cKldtXEH6UPnJpml8zHDKBU7+u54DH8PBZGFQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d116335c3fb153f8f822c794d86d5579')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route('/')
def home():
    return 'Hello World! LineBotEcho on Render'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)