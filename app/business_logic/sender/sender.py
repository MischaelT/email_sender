import random
import time
from typing import Dict, List


from business_logic.const import (GS, INITIAL, PREBID, text_choices)
from business_logic.data.data_manager import DataManager

from business_logic.mail.gmail_manager import GmailManager
from business_logic.sender.templates.email_templates import \
    generalAdvertisingTemplate
from business_logic.sender.templates.prebid_templates import prebidTemplate
from logger import logger
from models import Prospect, Website
from settings import TEST_MODE


class Sender:

    def __init__(self, manager: GmailManager, data_manager: DataManager) -> None:

        self.gmail_manager = manager
        self.data_manager = data_manager

        self.is_active: bool = False
        self.is_finished: bool = False

        self.current_website_info: dict = {}
        self.errors: list = []


    def run_sending(self) -> List[Website]:

        self.data_manager.backup_database()

        self.is_active = True
        websites_names = self.data_manager.initialize_email_data()
        self._send_emails(websites=websites_names)
        self.is_active = False

        self.is_finished = True

        self.data_manager.backup_logs()


    def _send_emails(self, websites: Dict[int, List[Website]]) -> List[Website]:

        logger.info('BEGIN PROCESS')
        logger.info('__________________________________________________________')

        exception_count = 0
        errored_websites: List[Website] = []

        for stage in websites:
            self.current_website_info['stage'] = text_choices[int(stage)]

            logger.info('__________________________________________________________')
            logger.info(f'Process {text_choices[int(stage)]} list')

            for website in websites[stage]:

                logger.info('__________________________________________________________')
                logger.info(f'Sending email to: {website.website_name}')

                self.current_website_info['current_website'] = website.website_name
                self.current_website_info['websites_left'] = f'{websites[stage].index(website)} from {len(websites[int(stage)])}'

                website_has_error = {}

                emails = self.data_manager.get_prospects(website.website_id)

                # if not emails:
                #     try:
                #         emails_to_db = self.finder.get_emails(website_domain=website.website_address)
                #     except Exception as exc:
                #         logger.error(exc)
                #         continue

                #     self.data_manager.push_prospects_to_db(website_address=website.website_address,
                #                                            data_to_push=emails_to_db)
                #     emails = self.data_manager.get_prospects(website.website_id)

                for email in emails:
                    self.current_website_info['exception_count'] = exception_count
                    self.current_website_info['current_email'] = email.email_address

                    generate_message_function = self._choose_template(website_type=website.website_type, stage=stage)

                    if stage == INITIAL:
                        email.last_message_id = None

                    try:
                        last_message_id = self.gmail_manager.send_email(generate_function=generate_message_function,
                                                                        website_name=website.website_address,
                                                                        email_to=email.email_address,
                                                                        reply_email_id=email.last_message_id)
                        logger.info(f'Email to {email.email_address} sent with id: {last_message_id}')
                    except Exception as ex:
                        exception_count += 1
                        website_has_error[email.email_address] = str(ex)
                        logger.info(f'There was an exception {ex}')
                        continue

                    self.data_manager.update_email(email, last_message_id)
                    self._wait_random(seconds=13)

                if not website_has_error.keys():
                    self.data_manager.update_website(website)
                    self.data_manager.update_user(stage=stage, emails_sent=len(emails))
                else:
                    errored_websites.append({website.website_address: website_has_error})

                self._wait_random(seconds=15)

            logger.info(f'Total websites in {text_choices[int(stage)]} list processed: {len(websites[int(stage)])}')
            logger.info('__________________________________________________________')

        logger.info('__________________________________________________________')
        logger.info('FINISH PROCESS')

        self.sending_errors = errored_websites

    def _choose_template(self, website_type, stage):
        if website_type == GS:
            return generalAdvertisingTemplate.get_message_generator(int(stage))
        elif website_type == PREBID:
            return prebidTemplate.get_message_generator(int(stage))

    def _wait_random(self, seconds: int) -> None:
        if not TEST_MODE:
            time.sleep(seconds + random.randint(1, 5))
