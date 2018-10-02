import logging

# https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
CRLB = "%0a"


def lambda_handler(event, context):
    to_number = event['To']
    from_number = event['From']
    logging.info(f'Received status request for {from_number}')

    return build_response(hangman()+f'{CRLB}{CRLB}'+letter_available())


def build_response(body):
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Sms>{body}</Sms></Response>'

#╔═══╗
#    ║
#    ║
#    ║
#════╝

def hangman():
    return f'╔═══╗{CRLB}    ║{CRLB}    ║{CRLB}    ║{CRLB}════╝'

def letter_available():
    return f'A B C D E F G H I J L M N{CRLB}O P Q R S T U V W X Y Z'
