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
from people_also_ask.google import get_related_questions
from typing import Optional

logger = logging.getLogger('app')


def paa(data):
    return json.dumps(get_related_questions(data['keyword'], data['hl'], data['gl'], data['zone'], config.PAA_MAX_QUESTIONS))


if __name__ == '__main__':
    configure_logging()

    app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/', debug=True)
    app.add_api('api.yaml')
    serve(TransLogger(app, setup_console_handler=False), host='0.0.0.0', port=8080, threads=config.PAA_THREADS,
          channel_timeout=config.PAA_CHANNEL_TIMEOUT, cleanup_interval=config.PAA_CLEANUP_INTERVAL)
