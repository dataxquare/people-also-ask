import os
from pathlib import Path

APP_ROOT = os.path.join(os.path.dirname(__file__))

FAST_ENV = os.getenv('FAST_ENV') or 'development'

ENVIRONMENTS = {
    'development': '.env.development',
    'production': '.env',
}

dotenv_path = os.path.join(APP_ROOT, ENVIRONMENTS.get(FAST_ENV) or '.env')