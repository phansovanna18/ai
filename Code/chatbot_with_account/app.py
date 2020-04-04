from fbchat import Client, log
from fbchat.models import *
import apiai
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import wikipedia
from user import *


def answer(message, bot):
    reply = bot.get_response(message)
    if reply.confidence < 0.7:
        reply = "I will tell the admin to train the message: "+message
    return reply


class JoWithMe(Client):
    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "Your Client Access Token"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'de'  # Default : English
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    def onMessage(self, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        # Chat Bot
        bot = ChatBot('Bot')
        trainer = ChatterBotCorpusTrainer(bot)
        trainer.train('greetings.yml')
        trainer.train('kit.yml')
        trainer.train('funny.yml')
        # reply message
        self.markAsRead(author_id)
        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))
        self.apiaiCon()
        msgText = message_object.text
        log.info(msgText)
        try:
            if 'wiki' in msgText.lower():
                reply = wikipedia.summary(msgText)
            else:
                reply = answer(msgText.lower(),bot)
        except Exception:
            reply = "Sorry, message not support for J+O ChatBot"
        if author_id != self.uid:
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
        self.markAsDelivered(author_id, thread_id)


client = JoWithMe(user, password)
client.listen()
