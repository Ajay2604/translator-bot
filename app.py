<<<<<<< HEAD
# Main 

=======
>>>>>>> parent of db1f673 (try with chatgpt)
import os
import sys
from argparse import ArgumentParser
import asyncio

from handlers.database import db
from handlers.prefered_language_handler import get_prefered_language, lang_update
from handlers.translate_text import translate_text, print_supported_languages

from flask import Flask, request, abort

from linebot import (
    WebhookParser
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ConfirmTemplate,
    PostbackAction    
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

    # if event is MessageEvent and message is TextMessage, then echo text //v2- removed echo
    for event in events:
        translated = ""
        print("event==>", event)
        langs = get_prefered_language(event.source)
        print("langs@81",langs)
        if not langs:
            # ask for language preference for first time
            translated = "Language setting failed try again with /lang \ne.g /lang en co "
            print("not langs")
            return
        
        # check /lang command
        text = event.message.text
        if(text is None):
            return
        
        if text[0,4]=="/lang":
            res = lang_update(event.source,text)
            print ("res==>", res)
            if not res:
                translated = "Language setting failed try again with /lang \ne.g /lang en co "
        elif text[0,4]=="/help":
            translated = f"set language by Giving Command /lang <> <> \n{print_supported_languages()}"
        else:
            #normal translation function
            print("else")
            translated = translate_text(text,langs)
            
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            res = line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=translated)]
                )
            )
            print("res==>", res)

    return 'OK'

print( __name__)
if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)