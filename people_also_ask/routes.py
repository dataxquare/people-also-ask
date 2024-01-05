from fastapi import APIRouter
from people_also_ask.google import get_related_questions
from people_also_ask.constants import PAA_MAX_QUESTIONS
from typing import Optional
from pydantic import BaseModel
import json

class PaaParams(BaseModel):
    keyword: str
    hl: str
    gl: str
    zone: Optional[str] = None

router = APIRouter()

@router.post("/paa")
def paa(data: PaaParams) -> str:
    paas = get_related_questions(data.keyword, data.hl, data.gl, data.zone, PAA_MAX_QUESTIONS)

    return json.dumps(paas)
