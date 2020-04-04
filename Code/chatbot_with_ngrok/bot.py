import requests,json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/v3.3/me/'


class Bot(object):
    def __init__(self,access_token, api_url=FACEBOOK_GRAPH_URL):
        self.access_token = access_token
        self.api_url = api_url

    def send_text_message(self, psid, message, messaging_type="RESPONSE"):
        print(self.access_token)
        print(psid)
        print(message)
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'messaging_type': messaging_type,
            'recipient': {"id": psid},
            'message': {"text": message}
        }

        params = {'access_token': self.access_token}
        self.api_url = self.api_url + 'messages'
        print(self.api_url)
        response = requests.post(self.api_url,
                                 params=params, headers=headers,
                                 data=json.dumps(data))
        print(headers)
        print(data)
        print(response.content)


bot = Bot('Page_Access_Token')
