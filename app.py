from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

# Load environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
MY_PHONE_NUMBER = os.getenv('MY_PHONE_NUMBER')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/sms", methods=['POST'])
def sms_reply():
    # Get incoming message details
    from_number = request.form['From']
    to_number = request.form['To']
    body = request.form['Body']

    # Initialize TwiML response
    resp = MessagingResponse()

    if from_number == MY_PHONE_NUMBER:
        # Message is from your personal number
        separator_position = body.find(':')

        if separator_position < 1:
            resp.message('You need to specify a recipient number and a ":" before the message. For example, "+12223334444: message".')
        else:
            recipient_number = body[:separator_position].strip()
            message_body = body[separator_position + 1:].strip()

            try:
                client.messages.create(
                    to=recipient_number,
                    from_=to_number,
                    body=message_body
                )
            except Exception as e:
                resp.message('There was an issue with the phone number you entered; please verify it is correct and try again.')
    else:
        # Message is from another number, forward it to your personal number
        client.messages.create(
            to=MY_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            body=f"{from_number}: {body}"
        )

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)