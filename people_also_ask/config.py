import os
from dotenv import load_dotenv

load_dotenv()

MAX_QUESTIONS = int(os.getenv('MAX_QUESTIONS', '10'))