import random
from app.config import FULL_NAME

from business_logic.const import FIRST, FOURTH, INITIAL, SECOND, THIRD
from business_logic.sender.templates.template import Template
from config import COMPANY_NAME, SHORT_NAME


class generalAdvertisingTemplate(Template):

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_message_generator(cls, stage):
        function_choices = {INITIAL: cls.generate_initial_email,
                            FIRST: cls.generate_first_followUp_email,
                            SECOND: cls.generate_second_followUp_email,
                            THIRD: cls.generate_third_followUp_email,
                            FOURTH: cls.generate_fourth_followUp_email}

        return function_choices[stage]

    @classmethod
    def generate_initial_email(cls: "generalAdvertisingTemplate", website_name: str) -> dict:

        """Generates an email text with given template

        Args:
            website_name (str): name of website

        Returns:
            dict: dict with keys: subject and text
        """

        greeting = random.choice(cls.greetings_list)

        initial_email = {'subject': f'Advertise Content From Your Website — {website_name} x {COMPANY_NAME}',
                         'text': f'''
{greeting}

I am {SHORT_NAME} from {COMPANY_NAME}

Best regards, {FULL_NAME}'''
                         }

        return initial_email

    @classmethod
    def generate_first_followUp_email(cls: "generalAdvertisingTemplate", website_name: str) -> dict:

        """Generates an email text with given template

        Args:
            website_name (str): name of website

        Returns:
            dict: dict with keys: subject and text
        """

        greeting = random.choice(cls.greetings_list)
        first_followUp_email = {'subject': f'Advertise Content From Your Website — {website_name} x {COMPANY_NAME}',
                                'text': f'''
{greeting}

I am {SHORT_NAME} from {COMPANY_NAME}

Best regards, {FULL_NAME}
                        '''
                                }

        return first_followUp_email

    @classmethod
    def generate_second_followUp_email(cls: "generalAdvertisingTemplate", website_name: str) -> dict:

        """Generates an email text with given template

        Args:
            website_name (str): name of website

        Returns:
            dict: dict with keys: subject and text
        """

        greeting = random.choice(cls.greetings_list)
        second_followUp_email = {'subject': f'Advertise Content From Your Website — {website_name} x {COMPANY_NAME}',
                                 'text': f'''
{greeting}

I am {SHORT_NAME} from {COMPANY_NAME}

Best regards, {FULL_NAME}
                                         '''
                                 }

        return second_followUp_email

    @classmethod
    def generate_third_followUp_email(cls: "generalAdvertisingTemplate", website_name: str) -> dict:

        """Generates an email text with given template

        Args:
            website_name (str): name of website

        Returns:
            dict: dict with keys: subject and text
        """

        greeting = random.choice(cls.greetings_list)
        third_followUp_email = {'subject': f'Advertise Content From Your Website — {website_name} x {COMPANY_NAME}',
                                'text': f'''
{greeting}

I am {SHORT_NAME} from {COMPANY_NAME}

Best regards, {FULL_NAME}
                                        '''
                                }

        return third_followUp_email

    @classmethod
    def generate_fourth_followUp_email(cls: "generalAdvertisingTemplate", website_name: str) -> dict:

        """Generates an email text with given template

        Args:
            website_name (str): name of website

        Returns:
            dict: dict with keys: subject and text
        """

        greeting = random.choice(cls.greetings_list)
        fourth_followUp_email = {'subject': f'Advertise Content From Your Website — {website_name} x {COMPANY_NAME}',
                                 'text': f'''
{greeting}

I am {SHORT_NAME} from {COMPANY_NAME}

Best regards, {FULL_NAME} for {website_name},

I am {SHORT_NAME} from {COMPANY_NAME}

Best regards, {FULL_NAME}
                                             '''}

        return fourth_followUp_email
