import logging


logging.basicConfig(format=u'%(asctime)s - %(levelname)s - %(module)s %(funcName)s - %(message)s',
                    level=logging.INFO,
                    filename='app.log',
                    filemode='w',
                    )

logger = logging.getLogger()
