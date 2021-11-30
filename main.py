import imaplib
import email
import os
import json
from ssl import ALERT_DESCRIPTION_UNEXPECTED_MESSAGE

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
resp_code, response = mail.login(USERNAME, PASSWORD)

print('\nLogging into Email...')
print(f'Response Code: {resp_code}')
print(f'Response: {USERNAME} - {response[0].decode()}') # Login verification

response, mailboxes = mail.list() # list of all mailboxes; tuple response, mailboxes

# Retrieve mailbox and mailbox mail count
print('\n============ List of Mailboxes and Mail Count =============\n')
for mailbox in mailboxes:
    mailbox_name = mailbox.decode().split('"')[-2]
    try:
        resp_code, mail_count = mail.select(mailbox_name)
        print(f'{mailbox_name} - {mail_count[0].decode()}')
    except Exception as e:
        print(f'{mailbox_name} - [CLIENTBUG]')
    
# Retrieve mailbox messages
resp_code, mail_count = mail.select('Inbox')
resp_code, mails = mail.search(None, 'ALL')
mail_ids = mails[0].decode().split()[-2:] # list of email IDs

for mail_id in mail_ids:
    print(f'\n====== Start of Mail {mail_id} ======\n')

    resp_code, mail_data = mail.fetch(mail_id, '(RFC822)') # fetch email contents: RFC822 pertains to email format
    message = email.message_from_bytes(mail_data[0][1]) # convert to readable message
    # Create email format
    print(f'From    : {message.get("From")}')
    print(f'To      : {message.get("To")}')
    print(f'Bcc     : {message.get("Bcc")}')
    print(f'Date    : {message.get("Date")}')
    print(f'Subject : {message.get("Subject")}')
    print(f'Body    : {message.get("Body")}')
    
    for message in message.walk(): # retrieve email body
        if message.get_content_type() == 'text/plain':
            body_lines = message.as_string().split('\n')
            print('\n'.join(body_lines))

    print(f'\n====== End of Mail {mail_id} ======\n')

mail.logout()
