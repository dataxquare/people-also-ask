import sys
# setting path
sys.path.append('./')

import connexion
import logging
import json
import config

from waitress import serve
from paste.translogger import TransLogger
from logger.logger import configure_logging
from google import get_related_questions

logger = logging.getLogger('app')


def paa(data):
    return json.dumps(get_related_questions(data['keyword'], data['hl'], data['gl'], config.PAA_MAX_QUESTIONS))


if __name__ == '__main__':
    configure_logging()

    app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/', debug=True)
    app.add_api('api.yaml')
    serve(TransLogger(app, setup_console_handler=False), host='0.0.0.0', port=8080)

