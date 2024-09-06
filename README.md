# Send and Receive SMS Anonymously Python

## Description

This Flask application serves as an SMS relay using Twilio. It allows you to use a Twilio phone number as a proxy for sending and receiving SMS messages, effectively masking your personal phone number from the public.
When the Twilio phone number associated with this application receives a message:

- If the message is from your personal number, it forwards the message to a specified recipient.
- If the message is from any other number, it relays the message to your personal number.

## Table of Contents

1. Installation
2. Configuration
3. Usage
4. License

## Installation

Clone this repository:

```sh
git clone https://github.com/twilio-samples/send-and-receive-sms-anonymously-python.git

cd twilio-sms-relay
```

Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages:

```sh
pip install -r requirements.txt
```

## Configuration

You will need a [Twilio Phone number](https://help.twilio.com/articles/223135247) and your Twilio Account SID and AUTH Token.
Set up the following environment variables, copy the `.env.example` and create a new `.env` file:

```
TWILIO_ACCOUNT_SID="your_account_sid"
TWILIO_AUTH_TOKEN="your_auth_token"
MY_PHONE_NUMBER="your_personal_number"
TWILIO_PHONE_NUMBER="your_twilio_number"
```

## Usage

Run the Flask application:

```sh
python app.py
```

The application will start on `http://127.0.0.1:5000/`.

Install ngrok: https://ngrok.com/download

In another terminal, start ngrok:

```sh
ngrok http 5000
```

Use the ngrok URL with `/sms` as the endpoint as your Twilio webhook URL, for example `https://xxxxxx.ngrok.app/sms`.

To send a message through the relay, text your Twilio number from your personal number with the format:

```
+1XXXXXXXXXX: Your message here
```

Replace `+1XXXXXXXXXX` with the recipient's phone number.
Any messages sent to your Twilio number will be forwarded to your personal number.

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
