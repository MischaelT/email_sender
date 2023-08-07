from abc import ABCMeta, abstractclassmethod, ABC
from typing import List


class Template(ABC):

    __metaclass__ = ABCMeta

    greetings_list: List[str] = ['Hi, ', 'Hello, ', 'Good afternoon, ']

    @abstractclassmethod
    def get_message_generator(cls, stage) -> callable:
        raise NotImplementedError("main method not implemented")

    @abstractclassmethod
    def generate_initial_email(cls, website_name: str) -> dict:
        raise NotImplementedError("main method not implemented")

    @abstractclassmethod
    def generate_first_followUp_email(cls, website_name: str) -> dict:
        raise NotImplementedError("main method not implemented")

    @abstractclassmethod
    def generate_second_followUp_email(cls, website_name: str) -> dict:
        raise NotImplementedError("main method not implemented")

    @abstractclassmethod
    def generate_third_followUp_email(cls, website_name: str) -> dict:
        raise NotImplementedError("main method not implemented")

    @abstractclassmethod
    def generate_fourth_followUp_email(cls, website_name: str) -> dict:
        raise NotImplementedError("main method not implemented")
