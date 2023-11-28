import os
import json
from dotenv import load_dotenv
from config import dotenv_path

load_dotenv(dotenv_path)

PAA_MAX_QUESTIONS = int(os.getenv('PAA_MAX_QUESTIONS', '10'))

try:
    SCRAPPER_HTTP_SERP_PROXY_AGENTS = json.loads(os.getenv("SCRAPPER_HTTP_SERP_PROXY_AGENTS", "[]"))
except:
    SCRAPPER_HTTP_SERP_PROXY_AGENTS = []

PAA_THREADS = int(os.getenv('PAA_THREADS', '4'))
PAA_CHANNEL_TIMEOUT = int(os.getenv('PAA_CHANNEL_TIMEOUT', '120'))
PAA_CLEANUP_INTERVAL = int(os.getenv('PAA_CLEANUP_INTERVAL', '30'))
