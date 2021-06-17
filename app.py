from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import get_dogs

app = Flask(__name__)

@app.route('/', methods=['POST'])
def incoming_sms():
    """
    Handles incoming text messages from Twilio API. 
    Isolates the text message and uses it to query The Dog API for a dog picture.
    Supports searching by breed and getting a random dog picture.
    return: url of a dog picture
    """
    txt = request.form['Body']

    # remove any spaces and make lowercase for query string formation
    txt = txt.lower()
    txt = txt.split()[0]

    # handle random searches differently than breed searches
    if txt == 'random':
        url = get_dogs.get_random_dog()
    else:
        url = get_dogs.request_breed(txt)
    
    resp = MessagingResponse()
    if url:
        resp.message(url)
    else:
        resp.message("Sorry! We couldn't find a dog matching that query. Please try \
        a more general search term.")
    return str(resp)


if __name__ == '__main__':
    app.run()
    