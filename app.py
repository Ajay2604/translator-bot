import os, re, json
from datetime import datetime, date, timedelta
from flask import Flask, request, abort
from googletrans import Translator
import requests
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
translator = Translator()

# channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_secret = "08b360ffb5ce55a583e1714f9ec01639"

# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_access_token = "b6QCoss7UIsWWEv0YjpiUZlRFGTEKOGxrQJ6ate4xMOfjRTaJSlaLP/yWi1G9Ry9y231IeERlfPgDy9exgigZYiheJy9wdGoe2+owPc1u1xK8PagSnpcll1dEnG6Ge4li46MwvbH+B1N+6jOGpfz4QdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%m-%d-%Y %H:%M%p")

    return """
    <h1>Hello Translator-Bot</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)

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

def translate_text(text):
    en_text = translator.translate(text, dest='en').text
    return en_text

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    translated = translate_text(text)
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=translated))
    

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
