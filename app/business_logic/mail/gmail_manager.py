import email.utils as eutils
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import Callable

from business_logic.const import HTML_signature
from config import FULL_NAME
from logger import logger
from settings import TEST_MODE


class GmailManager:
    def __init__(self, address, password) -> None:
        self.email_address: str = address
        self.password: str = password

    def send_email(self, generate_function: Callable, website_name: str, email_to: str, reply_email_id: str = None):

        email_id = self._generate_email_id(reply_email_id)

        message = generate_function(website_name=website_name)
        message_obj = self._construct_message(email_to, message, reply_email_id, email_id)

        if not TEST_MODE:
            self._send_message(message_obj)

        return email_id

    def _construct_message(self, email_to, message, reply_email_id, email_id) -> MIMEMultipart:

        msg = MIMEMultipart()
        msg['From'] = FULL_NAME
        msg['To'] = email_to
        msg['Subject'] = message['subject']
        msg["Message-ID"] = email_id

        if reply_email_id is not None:
            logger.info(f'In reply to {reply_email_id}')
            msg.add_header('In-Reply-To', reply_email_id)
            msg.add_header('References', reply_email_id)

        part1 = MIMEText(message['text'], 'plain')
        part2 = MIMEText(HTML_signature, 'html')

        with open(os.getcwd() + '/app/static/files/logo.png', 'rb') as fp:
            part3 = MIMEImage(fp.read())

        part3.add_header('Content-ID', '<image1>')

        msg.attach(part1)
        msg.attach(part2)
        msg.attach(part3)

        return msg

    def _send_message(self, message):
        with SMTP('smtp.gmail.com: 587') as server:
            server.starttls()
            server.login(self.email_address, self.password)
            server.sendmail(message['From'], message['To'], message.as_string())

    def _generate_email_id(self, reply_email_id):
        new_domain = 'mail.gmail.com'
        if reply_email_id is None:
            email_id = eutils.make_msgid(domain=new_domain)
        else:
            current_domain = str.split(str.split(reply_email_id, '@')[1], '>')[0]

            if current_domain == new_domain:
                email_id = eutils.make_msgid(domain=new_domain)
            else:
                email_id = eutils.make_msgid(domain='MY-DOMAIN')
            
            logger.info('Generating email id')
        return email_id

    def _get_unread_messages(self):
        pass

    def _determine_auto_reply(self):
        pass

    def _determine_bad_addresses():
        pass
