import asyncio
from typing import Union

from business_logic.api_accessors.snow_io_api import SnowIoAPI
from business_logic.checker.check_manager import CheckManager
from business_logic.checker.checkers.file_checker import FileChecker
from business_logic.checker.checkers.server_checker import ServerChecker
from business_logic.checker.checkers.similarWeb_checker import \
    SimilarWebChecker
from business_logic.checker.checkers.snowIo_checker import SnowIOChecker
from business_logic.checker.checkers.weird_checker import WeirdChecker
from business_logic.data.data_manager import DataManager
from business_logic.finder.finder import EmailFinder
from business_logic.mail.gmail_manager import GmailManager
from business_logic.sender.sender import Sender
from config import EMAIL, PASSWORD, SNOW_IO_API_PUBLIC, SNOW_IO_API_SECRET
from logger import logger
from models import db

from csv import writer


class AppManager:

    def __init__(self) -> None:

        snow_io_api_accessor = SnowIoAPI(public_key=SNOW_IO_API_PUBLIC, secret_key=SNOW_IO_API_SECRET)
        self.finder = EmailFinder(snow_api=snow_io_api_accessor)

        self.data_manager = DataManager(database=db)
        self.gmail_manager = GmailManager(address=EMAIL, password=PASSWORD)

        self.checker = CheckManager(snow_io=SnowIOChecker(snow_io_api_accessor),
                                    similar_web=SimilarWebChecker(),
                                    file_checker=FileChecker(),
                                    server_checker=ServerChecker(),
                                    weird_checker=WeirdChecker())

        self.send_manager = Sender(manager=self.gmail_manager,
                                   checker=self.checker,
                                   data_manager=self.data_manager,
                                   finder=self.finder)
        
        self.today = None

    def set_up_today(self, today):
        self.today = today
        self.data_manager.today = today

    def get_status(self, manager: Union[Sender, CheckManager]):
        return manager.current_website_info, manager.errors

    def clear_status(self, manager: Union[Sender, CheckManager]):
        manager.current_website_info = {}
        manager.errors = []

    def run_parsing(self, path_to_file, website_type):
        self.clear_status(self.checker)


        self.checker.is_active = True
        try:
           passed, not_passed = asyncio.run(self.checker.run_async_parse(path_to_file=path_to_file))
        except Exception as exc:
            logger.error(exc)
            raise Exception
        finally:
            self.checker.is_active = False
            self.checker.is_finished = True

        if not_passed:
            logger.info('Not passsed websites')
            for np in not_passed:
                logger.info(np)

        if passed:
            self.data_manager.push_websites_to_db(data_to_push=passed, website_type=website_type)

        if self.checker.errors:
            for row in self.checker.errors:
                with open('errors.csv', 'a', newline='') as file:
                    wr = writer(file)
                    wr.writerow([list(row.keys())[0], list(row.values())[0]])
