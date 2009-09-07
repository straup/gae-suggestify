from config import config
from google.appengine.api import mail

def is_valid_address (address) :
    return mail.is_email_valid(address)
        
def send (**kwargs) :

    from_addr = config['notifications_sender']

    # wrap me...
    body = kwargs['body']

    try :
        mail.send_mail(sender=from_addr, to=kwargs['to'], subject=kwargs['subject'], body=body)    
    except Exception, e :
        return False

    return True
