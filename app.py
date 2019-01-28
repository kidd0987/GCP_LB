from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('PEd9sD8sCMrD18H2m/rmhzow2T8gYwMld8tYlKEcjQod2kmpqX05Mquu7cf7G998zEuP4hrUAyicgJ1Ga++8U27cgSjZcgkj+qqU59SDyHfq4I7WU8pne07TDpeP76q+9cRlDhZHKAQHK4hTLzCT7QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4db6bb4896e8b4d280c08fdc84ee4483')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
