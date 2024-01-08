import logging
from typing import Optional
from fastapi import APIRouter
import json
from people_also_ask.google import get_related_questions
from people_also_ask.constants import PAA_MAX_QUESTIONS
from pydantic import BaseModel

class PaaParams(BaseModel):
    keyword: str
    hl: str
    gl: str
    zone: Optional[str] = None

router = APIRouter()
logger = logging.getLogger('app')

@router.post("/paa")
def paa(data: PaaParams) -> str:
    logger.info('People Also Ask service started for %s, %s, %s and %s', data.keyword, data.hl, data.gl, data.zone)
    paas = get_related_questions(data.keyword, data.hl, data.gl, data.zone, PAA_MAX_QUESTIONS)

    logger.info('People also ask service end with %s paas for %s, %s, %s and %s', len(paas), data.keyword, data.hl, data.gl, data.zone)
    return json.dumps(paas)
