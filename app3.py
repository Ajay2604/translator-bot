#trial

import aiohttp
from aiohttp import web
import json
import os

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

async def handle(request):
    request_json = await request.json()
    print(request_json)

    # Extract necessary information from the request
    reply_token = request_json['events'][0]['replyToken']
    message_text = request_json['events'][0]['message']['text']

    # Your bot logic goes here
    reply_message = f"You said: {message_text}"

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
    app.router.add_post('/callback', handle)

    import os
    port = int(os.environ.get("PORT", 8080))

    web.run_app(app, host='0.0.0.0', port=port)