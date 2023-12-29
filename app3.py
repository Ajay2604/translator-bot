#trial

import aiohttp
from aiohttp import web
import json
import os
import icecream
from datetime import datetime, date, timedelta

from handlers.database import db
from handlers.prefered_language_handler import get_prefered_language, lang_update
from handlers.translate_text import translate_text, print_supported_languages


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

async def revertMessage(source, msg):
    if msg is None:
        return

    # check /lang command
    words = msg.split()
    if words[0]=="/lang":
        print("langs set")
        res = await lang_update(source,msg)
        print ("res==>", res)
        if not res:
            return "Language setting failed try again with /lang \ne.g /lang en co "
        else:
            return f"Language setting complete for {words[1]} & {words[2]}"
    elif words[0]=="/help":
        print("langs help")
        return f"set language by giving Command /lang <> <> \n{print_supported_languages()}"
    else:
        #normal translation function
        langs = await get_prefered_language(source)
        print("langs@21",langs)
        if not langs:
        # ask for language preference for first time
            print("not langs")
            return "\nEn-ko are set as Default languages.\nTo Change the default settings, send command  /lang <> <> \ne.g /lang en ko\nFor list of languages type /help"
        print("else")
        return await translate_text(msg,langs)

async def homepage(request):

    the_time = datetime.now().strftime("%m-%d-%Y %H:%M%p")
    page_content ="""
    <h1>Hello Translator-Bot</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)
    return web.Response(text=page_content, content_type='text/html')

async def handle(request):
    request_json = await request.json()
    print(request_json)

    # Extract necessary information from the request
    reply_token = request_json['events'][0]['replyToken']
    message_text = request_json['events'][0]['message']['text']
    source = request_json['events'][0]['source']
    # Your bot logic goes here
    # reply_message = f"You said: {message_text}"
    reply_message = await revertMessage(source,message_text)

    # Send the reply message
    await reply(reply_token, reply_message)

    return web.Response()

async def reply(reply_token, reply_message):
    line_api_url = 'https://api.line.me/v2/bot/message/reply'
    access_token = channel_access_token  # Replace with your Line bot access token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'text',
                'text': reply_message
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(line_api_url, headers=headers, data=json.dumps(data)) as response:
            return await response.text()

if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', homepage)
    app.router.add_post('/callback', handle)

    port = int(os.environ.get("PORT", 8080))

    web.run_app(app, host='0.0.0.0', port=port)
