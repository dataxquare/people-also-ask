import json
import logging
import sys

import connexion
from config import (PAA_CHANNEL_TIMEOUT, PAA_CLEANUP_INTERVAL,
                    PAA_MAX_QUESTIONS, PAA_THREADS)
from google import get_related_questions
from logger.logger import configure_logging
from paste.translogger import TransLogger
from waitress import serve

# setting path
sys.path.append('./')


logger = logging.getLogger('app')


def paa(data):
    return json.dumps(get_related_questions(data['keyword'], data['hl'], data['gl'], PAA_MAX_QUESTIONS))


if __name__ == '__main__':
    configure_logging()

    app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/', debug=True)
    app.add_api('api.yaml')
    serve(TransLogger(app, setup_console_handler=False), host='0.0.0.0', port=8080, threads=PAA_THREADS,
          channel_timeout=PAA_CHANNEL_TIMEOUT, cleanup_interval=PAA_CLEANUP_INTERVAL)
