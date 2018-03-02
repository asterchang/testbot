
import os, sys
from wit import Wit

WIT_ACCESS_TOKEN = os.environ["WIT_ACCESS_TOKEN"]
client = Wit(access_token = WIT_ACCESS_TOKEN)


def wit_response(message_text):
    resp = client.message(message_text)

    entity = None
    value = None

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except:
        pass

    return (entity, value)

