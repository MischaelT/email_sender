import os
import shutil
from typing import Dict, List

from business_logic.const import (FIRST, FOURTH, INITIAL, SECOND, THIRD,
                                  days_to_add_choices)
from business_logic.data.validators import is_empty, is_valid
from business_logic.mics import date_by_adding_business_days
from config import SHORT_NAME
from flask_sqlalchemy import SQLAlchemy
from logger import logger
from models import Prospect, Users, Website
from settings import BASEDIR


class DataManager:
    def __init__(self, database) -> None:

        self.errored_rows = {'error_in_email': [],
                             'email_already_in_db': [],
                             'website_already_in_db': []}

        self._db = database

    @property
    def today(self):
        return self._today

    @today.setter
    def today(self, today):
        self._today = today

    @property
    def database(self):
        pass

    @database.setter
    def database(self, database: SQLAlchemy):
        self._db = database

    def make_fields_empty(self) -> None:
        for key in self.errored_rows:
            self.errored_rows[key] = []

    def push_websites_to_db(self, data_to_push: list, website_type: str) -> None:
        for website_address in data_to_push:
            logger.info(f'pushing {website_address} to db')
            if self._website_in_database(website_address):
                logger.info(f'Website {website_address} already in db')
                self.errored_rows['website_already_in_db'].append(website_address)
                continue
            self._write_website_to_db(website_address, website_type, stage=None)

    def push_prospects_to_db(self, data_to_push: list, website_address: str) -> None:
        logger.info(f'Pushing prospects of website {website_address} to database')
        website_id = self._db.session.query(Website.website_id).filter_by(website_address=website_address).first()[0]

        for prospect in data_to_push:
            logger.info(f'pushing {prospect} to database')
            
            if self._prospect_in_database(prospect, website_id):
                logger.info(f'{prospect} already in database')
                self.errored_rows['email_already_in_db'].append(prospect)
                continue

            if not is_valid(prospect) or is_empty(prospect):
                logger.info(f'{prospect} email is not valid')
                self.errored_rows['error_in_email'].append(prospect)
                continue
            self._write_prospect_to_db(prospect, website_id)

    def get_prospects(self, website_id):
        return Prospect.get_prospects_by_website_id(self._db.session, website_id)

    def initialize_email_data(self) -> Dict[int, List[Website]]:

        logger.info('Initialising data before sending')

        websites_names_to_show = {INITIAL: [], FIRST: [], SECOND: [], THIRD: [], FOURTH: []}
        website_data = Website.websites_by_isActive_nextEmailDate(self._db.session, int(True), self.today)

        for website in website_data:
            stage = int(website.stage)
            websites_names_to_show[stage].append(website)

        return websites_names_to_show

    def update_email(self, email_to_update: Prospect, last_message_id: str) -> None:
        email_to_update.last_message_id = last_message_id
        self._db.session.commit()

    def update_website(self, website_to_update: Website) -> None:

        if int(website_to_update.stage) == FOURTH:
            logger.info(f'Move website: {website_to_update.website_name} to history DB')
            website_to_update.next_email_date = date_by_adding_business_days(from_date=str(self.today), add_days=80)
            website_to_update.process_is_active = int(False)
            website_to_update.process_start_date = None
            website_to_update.stage = None
            self._db.session.commit()
            return

        next_email_date = date_by_adding_business_days(from_date=website_to_update.process_start_date,
                                                       add_days=days_to_add_choices[int(website_to_update.stage)])

        website_to_update.stage = int(website_to_update.stage) + 1
        website_to_update.next_email_date = next_email_date
        self._db.session.commit()

    def update_user(self, stage: int, emails_sent: int) -> None:
        user = Users.get_user_by_name(self._db.session, SHORT_NAME)
        if stage == INITIAL:
            user.websites_processed = int(user.websites_processed) + 1
        else:
            user.emails_sent = int(user.emails_sent) + emails_sent
        self._db.session.commit()

    def _write_website_to_db(self, website_address: str, website_type: str, stage: int) -> None:

        website_name = self._make_name(website_address)

        website = Website(website_name=website_name,
                          website_address=website_address,
                          creation_date=self.today,
                          process_is_active=int(False),
                          process_start_date=None,
                          stage=None,
                          next_email_date=self.today,
                          website_type=website_type)

        self._db.session.add(website)
        self._db.session.commit()

    def _write_prospect_to_db(self, prospect: str, website_id: str) -> None:

        email_data = Prospect(website_id=website_id,
                              email_address=prospect,
                              last_message_id=None)

        self._db.session.add(email_data)
        self._db.session.commit()

    # TODO Re-write method to get wid of such websites: www.es.slideshare.com
    def _make_name(self, website_address: str) -> str:
        website_address = website_address.lower()
        website_name_parts = website_address.split(sep='.')
        if website_name_parts[0] == 'www':
            return website_name_parts[1]
        return website_name_parts[0]

    def _website_in_database(self, website_address: str) -> bool:
        website_in_database = self._db.session.query(Website.website_name).filter_by(website_address=website_address).first() is not None  # noqa
        return website_in_database

    def _prospect_in_database(self, prospect_email: str, website_id: int) -> bool:
        prospect_in_database = self._db.session.query(Prospect.email_address).filter_by(email_address=prospect_email).first() is not None  # noqa
        return prospect_in_database

    def backup_logs(self) -> None:
        path_to_log_file = os.path.join(BASEDIR, 'app.log')
        if os.path.exists(path_to_log_file):
            destination_path = os.path.join(BASEDIR, 'app', 'logs', f'{self.today}.log')
            shutil.copy2(path_to_log_file, destination_path)

    def backup_database(self) -> None:
        path_to_db_file = os.path.join(BASEDIR, 'websites.db')
        if os.path.exists(path_to_db_file):
            destination_path = os.path.join(BASEDIR, 'app', 'logs', f'{self.today}.db')
            shutil.copy2(path_to_db_file, destination_path)
