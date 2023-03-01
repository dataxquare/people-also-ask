import os
import json
from dotenv import load_dotenv

load_dotenv()

PAA_MAX_QUESTIONS = int(os.getenv('PAA_MAX_QUESTIONS', '10'))

try:
    SCRAPPER_HTTP_SERP_PROXY_AGENTS = json.loads(os.getenv("SCRAPPER_HTTP_SERP_PROXY_AGENTS", "[]"))
except:
    SCRAPPER_HTTP_SERP_PROXY_AGENTS = []
