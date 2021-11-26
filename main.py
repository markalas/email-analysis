import imaplib
import os
import json

# Set working directory
CURR_DIR = os.curdir

# Get email credentials from email.json
CREDENTIALS = open(os.path.join(CURR_DIR, 'email.json'))
LOGIN = json.load(CREDENTIALS)
USERNAME = LOGIN['email'][0]['address']
PASSWORD = LOGIN['email'][0]['password']

# Connect to email

yahooSmtpServer = 'imap.mail.yahoo.com'
yahooSmtpPort = 993
mail = imaplib.IMAP4_SSL(yahooSmtpServer, yahooSmtpPort)
mail.login(USERNAME, PASSWORD)
print(mail.list())
mail.logout()