# translator-bot
LINE Messaging API Translator Bot
Copy code
# Line Bot - Google Translate

This project is a simple Line Bot that can translate English to French or French to English using the Google Translate API. The bot listens for user messages and replies with the translated text.

## Prerequisites

1. A Google Cloud account: To use the Google Translate API, you need a Google Cloud account.
2. A Line account: To create a Line Bot, you need a Line account.

## Setup

1. Clone this repository to your local machine:

```bash
git clone https://github.com/username/line-bot-google-translate.git
Create a virtual environment and activate it:
bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install the required packages:
bash
Copy code
pip install -r requirements.txt
Set up your Google Cloud API key and the Google Translate API.

Set up your Line Bot. Follow the official documentation for details: https://developers.line.biz/en/docs/messaging-api/getting-started/

Export the necessary environment variables for your Google Cloud API key and your Line Bot channel secret and access token.

bash
Copy code
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-cloud-api-key.json
export LINE_CHANNEL_SECRET=your-line-channel-secret
export LINE_CHANNEL_ACCESS_TOKEN=your-line-channel-access-token
Run the Flask app:
bash
Copy code
python app.py
Usage
To use the bot, simply add it as a friend on the Line app and start sending messages. The bot will automatically translate the text from English to French or French to English and send it back to you.

Copy code
1. Start a conversation with the bot on the Line app.
2. Type your message in English or French.
3. The bot will reply with the translated text.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Copy code

Remember to replace "username" in the git clone URL with your actual GitHub username. Additionally, replace "your-line-channel-secret" and "your-line-channel-access-token" with your actual Line Bot channel secret and access token.


