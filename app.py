"""
Twilio SMS Relay Flask Application

Description: This Flask application acts as an SMS relay using Twilio.
When the associated Twilio phone number receives a message, it either
forwards the message to a specified number or relays it to your personal number.

Contents:
1. Imports and Setup
2. Environment Variables
3. Main Handler (sms_reply function)
4. Application Entry Point
"""

# 1. Imports and Setup
#
# Here we import the necessary libraries and initialize our Flask application.
# We also set up the Twilio client for making API calls.

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


# 2. Environment Variables
#
# We load the necessary credentials and phone numbers from environment variables.
# This keeps sensitive information out of the code and allows for easier configuration
# across different environments.

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
MY_PHONE_NUMBER = os.getenv('MY_PHONE_NUMBER')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# 3. Main Handler (sms_reply function)
#
# This is the main entry point of our application. It handles incoming SMS messages
# and determines how to process them based on the sender's number.
# If the message is from your personal number, it parses the message to send to another recipient.
# If the message is from any other number, it forwards the message to your personal number.

@app.route("/sms", methods=['POST'])
def sms_reply():
    # Extract incoming message details
    from_number = request.form['From']
    to_number = request.form['To']
    body = request.form['Body']

    # Initialize TwiML response
    resp = MessagingResponse()

    if from_number == MY_PHONE_NUMBER:
        # Message is from your personal number
        separator_position = body.find(':')

        if separator_position < 1:
            # If the message format is incorrect, send an instructional message back
            resp.message('You need to specify a recipient number and a ":" before the message. For example, "+12223334444: message".')
        else:
            # Parse the recipient number and message body
            recipient_number = body[:separator_position].strip()
            message_body = body[separator_position + 1:].strip()

            try:
                # Attempt to send the message using Twilio client
                client.messages.create(
                    to=recipient_number,
                    from_=to_number,
                    body=message_body
                )
            except Exception as e:
                # If there's an error (e.g., invalid phone number), send an error message back
                resp.message('There was an issue with the phone number you entered; please verify it is correct and try again.')
    else:
        # Message is from another number, forward it to your personal number
        client.messages.create(
            to=MY_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            body=f"{from_number}: {body}"
        )

    # Return the TwiML response
    return str(resp)

# 4. Application Entry Point
#
# This section runs the Flask application when the script is executed directly.
# The debug mode is set to True, which is useful for development but should be set to False in production.
if __name__ == "__main__":
    app.run(debug=True)