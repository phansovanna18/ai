from fbchat import Client, log
from fbchat.models import *
import apiai, codecs, json
import credentials

class JoWithME(Client):
    # to connect with Dialogflow
    def apiaiCon(self):
            #linking token from Dialogflow
            self.CLIENT_ACCESS_TOKEN = "1395d086863d4dd28317cef996efd7f8"
            self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
            self.request = self.ai.text_request()
            self.request.lang = 'de'
            self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    def onMessage(
        self,
        author_id=None,
        message_object=None,
        thread_id=None,
        thread_type=ThreadType.USER,
        **kwargs
    ):
        #mark message as read
        self.markAsRead(author_id)

        #print message to console
        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))

        #establishing connection using apiai module
        self.apiaiCon()

        #getting message
        msgText = message_object.text

        #request query/reply for the msg received
        self.request.query = msgText

        #getting the response as json object
        response = self.request.getresponse()

        #convert json object to a list
        obj = json.load(response)

        #getting reply from the converted list
        reply = obj['result']['fulfillment']['speech']

        #sending the message
        if author_id != self.uid:
            self.send(Message(text=reply), thread_id = thread_id, thread_type = thread_type)

        #mark message as delivered
        self.markAsDelivered(author_id, thread_id)

#creating an objectof our class and passing arguments as our email and password
client = JoWithME(credentials.myfb["email"], credentials.myfb["password"])

#listening for new message
client.listen()
