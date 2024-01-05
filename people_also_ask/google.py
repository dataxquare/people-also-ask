#! /usr/bin/env python3
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Generator
import uule_grabber

from people_also_ask.parser import (
    extract_related_questions,
    get_featured_snippet_parser,
)
from people_also_ask.exceptions import (
    RelatedQuestionParserError,
    FeaturedSnippetParserError
)
from people_also_ask.request.session import get

logger = logging.getLogger('app')


URL = "https://www.google.com/search"


def search(keyword: str, hl: Optional[str] = "en", gl: Optional[str] = "us", zone: Optional[str] = None) -> Optional[BeautifulSoup]:
    """return html parser of google search result"""
    params = {"q": keyword, "hl": hl, "gl": gl}

    if zone:
        uule = uule_grabber.uule(zone)
        params["uule"] = uule
        
    response = get(URL, params=params)

    return BeautifulSoup(response.text, "html.parser")


def _get_related_questions(text: str, hl: Optional[str] = "en", gl: Optional[str] = "us", zone: Optional[str] = None) -> List[str]:
    """
    return a list of questions related to text.
    These questions are from search result of text

    :param str text: text to search
    :param str hl: language to search
    :param str gl: geo to search
    """
    document = search(text, hl, gl, zone)
    if not document:
        return []
    try:
        return extract_related_questions(document)
    except Exception:
        raise RelatedQuestionParserError(text, hl, gl)


def generate_related_questions(text: str, hl: Optional[str] = "en", gl: Optional[str] = "us") -> Generator[str, None, None]:
    """
    generate the questions related to text,
    these quetions are found recursively

    :param str text: text to search
    :param str hl: language to search
    :param str gl: geo to search
    """
    logger.info("generate_related_questions init")
    questions = set(_get_related_questions(text, hl, gl))
    searched_text = set(text)
    while questions:
        text = questions.pop()
        yield text
        searched_text.add(text)
        questions |= set(_get_related_questions(text, hl, gl))
        questions -= searched_text


def get_related_questions(text: str, hl: Optional[str] = "en", gl: Optional[str] = "us", zone: Optional[str] = None,
                          max_nb_questions: Optional[int] = None):
    """
    return a number of questions related to text.
    These questions are found recursively.

    :param str text: text to search
    :param str hl: language to search
    :param str gl: geo to search
    :param int max_nb_questions: max number of questions
    """
    logger.info("get_related_questions for: " + ','.join([text, hl, gl]) + " init")
    questions = set(_get_related_questions(text, hl, gl, zone))

    if max_nb_questions is None or max_nb_questions <= len(questions):
        return list(questions)
    else:
        searched_text = set(text)
        while questions:
            text = questions.pop()
            searched_text.add(text)
            questions |= set(_get_related_questions(text, hl, gl))
            questions -= searched_text
            if max_nb_questions <= len(questions):
                return list(questions)
                
        return list(questions)

def get_answer(question: str) -> Dict[str, Any]:
    """
    return a dictionary as answer for a question.

    :param str question: asked question
    """
    document = search(question)
    related_questions = extract_related_questions(document)
    featured_snippet = get_featured_snippet_parser(
            question, document)
    if not featured_snippet:
        res = dict(
            has_answer=False,
            question=question,
            related_questions=related_questions,
        )
    else:
        res = dict(
            has_answer=True,
            question=question,
            related_questions=related_questions,
        )
        try:
            res.update(featured_snippet.to_dict())
        except Exception:
            raise FeaturedSnippetParserError(question)
    return res


def generate_answer(text: str) -> Generator[dict, None, None]:
    """
    generate answers of questions related to text

    :param str text: text to search
    """
    answer = get_answer(text)
    questions = set(answer["related_questions"])
    searched_text = set(text)
    if answer["has_answer"]:
        yield answer
    while questions:
        text = questions.pop()
        answer = get_answer(text)
        if answer["has_answer"]:
            yield answer
        searched_text.add(text)
        questions |= set(get_answer(text)["related_questions"])
        questions -= searched_text


def get_simple_answer(question: str, depth: bool = False) -> str:
    """
    return a text as summary answer for the question

    :param str question: asked quetion
    :param bool depth: return the answer of first related question
        if no answer found for question
    """
    document = search(question)
    featured_snippet = get_featured_snippet_parser(
            question, document)
    if featured_snippet:
        return featured_snippet.response
    if depth:
        related_questions = get_related_questions(question)
        if not related_questions:
            return ""
        return get_simple_answer(related_questions[0])
    return ""
