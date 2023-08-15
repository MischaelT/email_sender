import asyncio

from business_logic.data.data_manager import DataManager
from business_logic.mail.gmail_manager import GmailManager
from business_logic.sender.sender import Sender
from config import EMAIL, PASSWORD
from logger import logger
from models import db

from csv import writer


class AppManager:

    def __init__(self) -> None:

        self.data_manager = DataManager(database=db)
        self.gmail_manager = GmailManager(address=EMAIL, password=PASSWORD)

        self.send_manager = Sender(manager=self.gmail_manager,
                                   data_manager=self.data_manager)
        
        self.today = None

    def set_up_today(self, today):
        self.today = today
        self.data_manager.today = today

    def get_status(self, manager: Sender):
        return manager.current_website_info, manager.errors

    def clear_status(self, manager: Sender):
        manager.current_website_info = {}
        manager.errors = []

    # def run_parsing(self, path_to_file, website_type):
    #     self.clear_status(self.checker)

    #     self.checker.is_active = True
    #     try:
    #        passed, not_passed = asyncio.run(self.checker.run_async_parse(path_to_file=path_to_file))
    #     except Exception as exc:
    #         logger.error(exc)
    #         raise Exception
    #     finally:
    #         self.checker.is_active = False
    #         self.checker.is_finished = True

    #     if not_passed:
    #         logger.info('Not passsed websites')
    #         for np in not_passed:
    #             logger.info(np)

    #     if passed:
    #         self.data_manager.push_websites_to_db(data_to_push=passed, website_type=website_type)

    #     if self.checker.errors:
    #         for row in self.checker.errors:
    #             with open('errors.csv', 'a', newline='') as file:
    #                 wr = writer(file)
    #                 wr.writerow([list(row.keys())[0], list(row.values())[0]])
