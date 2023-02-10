import os
import json
from dotenv import load_dotenv

load_dotenv()

MAX_QUESTIONS = int(os.getenv('MAX_QUESTIONS', '10'))

SCRAPPER_USER_AGENT = os.getenv(
    'SCRAPPER_USER_AGENT',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
)

try:
    SCRAPPER_HTTP_SERP_PROXY_AGENTS = json.loads(os.getenv("SCRAPPER_HTTP_SERP_PROXY_AGENTS", "[]"))
except:
    SCRAPPER_HTTP_SERP_PROXY_AGENTS = []