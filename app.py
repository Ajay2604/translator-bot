import os
import sys
from argparse import ArgumentParser
from googletrans import Translator
translator = Translator()

from flask import Flask, request, abort
from linebot import (
    WebhookParser
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from datetime import datetime, date, timedelta

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

parser = WebhookParser(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

def translate_text(text): # translate text to/from Korean and English
    srcLang = translator.detect(text).lang # detect the source language
    if(srcLang=="ko"): # if the source language is Korean
        return translator.translate(text, dest='en').text # translate to English
    elif (srcLang=="en"): # if the source language is English
        return translator.translate(text, dest='ko').text # translate to Korean
    else: # if the source language is neither Korean nor English
        return "Language is not set up for detected language" # return an error message

@app.route('/')
def homepage():
    # Get current time
    the_time = datetime.now().strftime("%m-%d-%Y %H:%M%p")
    
    # Render HTML template with time and image
    return """
    <h1>Hello Translator-Bot</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echp text // removed echo
    for event in events:
        # if not isinstance(event, MessageEvent):
        #     print("not a MessageEvent")
        #     # continue
        # if not isinstance(event.message, TextMessageContent):
        #     print("not a TextMessageContent")
        #     # continue
        # print("event==>", event)
        text = event.message.text
        # print("text==>", text)
        translated = ""
        if(text is not None):
                translated = translate_text(text)
                # print("translated==>",translated)
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=translated)]
                )
            )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)