from flask import Flask, request
import json
from bot import Bot


PAGE_ACCESS_TOKEN = 'Page_Access_Token'
GREETINGS = ['Hi','Hello', 'Hi there', 'Hey', 'hey', 'Hola', 'hi', 'hello', 'hi there', 'how are you?', 'hola', 'Heyo']
BYE = ['bye', 'c\'ya', 'goodbye', 'see you later', 'bye bye']

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == 'secret':
            return str(challenge)
        return '400'
    else:
        print(request.data)
        data = json.loads(request.data)
        messaging_events = data['entry'][0]['messaging']
        bot = Bot(PAGE_ACCESS_TOKEN)
        for message in messaging_events:
            user_id = message['sender']['id']
            text_input = message['message'].get('text')
            response_text = "I'm still learning..."
            if text_input in GREETINGS:
                response_text = "Hello. I'm chatbot what can I help you?"
            if text_input in BYE:
                response_text = "goodbye! have a good day..."
            if text_input == 'ily' or text_input == "i love you" or text_input == "I love u":
                response_text = "I love u, too sweetie"
            print(user_id, text_input)
            bot.send_text_message(user_id, response_text)

        return '200'


if __name__ == '__main__':
    app.run(debug=True)
