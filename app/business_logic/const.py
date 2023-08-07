from app.config import COMPANY_PHONE
from config import EMAIL, FULL_NAME, POSITION, COMPANY_WEBSITE, COMPANY_ADDRESS


INITIAL = 0
FIRST = 1
SECOND = 2
THIRD = 3
FOURTH = 4

text_choices = {INITIAL: 'initial email',
                FIRST: 'first FollowUp email',
                SECOND: 'second FollowUp email',
                THIRD: 'third FollowUp email',
                FOURTH: 'fourth FollowUp email'}

days_to_add_choices = {INITIAL: 1,
                       FIRST: 3,
                       SECOND: 5,
                       THIRD: 10}

signature_texts = [f'{FULL_NAME} / {POSITION} / {COMPANY_WEBSITE}',
                   f'{COMPANY_ADDRESS}  |  {COMPANY_PHONE} |  {EMAIL} |',
                   f'Email:  {EMAIL}',
]

HTML_signature = f'''
                        <br>
                        <br>
                        <table>
                            <tr>
                                <td rowspan ="3">
                                  <img src="cid:image1">
                                </td>
                                <td>{signature_texts[0]}</td>
                            </tr>
                            <tr>
                                <td>{signature_texts[1]}</td>
                            </tr>
                            <tr>
                                <td>{signature_texts[2]}</td>
                            </tr>
                            <br>
                            <tr>
                                <td>{signature_texts[3]}{signature_texts[4]}</a></td>
                            </tr>
                        </table>
                    '''  # noqa

GS = 'GS'
PREBID = 'prebid'

WORK = 'work'
HISTORY = 'history'
