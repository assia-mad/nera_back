from urllib import response
import firebase_admin
from firebase_admin import credentials , messaging
from nera_pro import settings


# cred = credentials.Certificate(settings.credentials)
# firebase_admin.initialize_app(cred)

def sendPush(title , msg ):

        notification= messaging.Notification(title=title,
                                             body=msg,  
    )


