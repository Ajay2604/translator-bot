from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests

app = Flask(__name__)

# LINE bot info
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# Google Translate API endpoint
translate_url = "https://translation.googleapis.com/language/translate/v2"

# Callback function to handle received messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Extract the original message and the target language
    original_message = event.message.text
    target_language = 'en' # or any other target language code

    # Translate the original message
    headers = {"Content-Type": "application/json"}
    data = {
        "q": original_message,
        "target": target_language,
        "format": "text"
    }
    response = requests.post(translate_url, headers=headers, data=json.dumps(data))
    translation = response.json()['data']['translations'][0]['translatedText']

    # Send the translated message back to the user
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translation)
    )

# Webhook URL for LINE bot
@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook events
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run()