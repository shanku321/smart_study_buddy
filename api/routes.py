from fastapi import APIRouter
from pydantic import BaseModel

from services.quiz_generator import generate_quiz
from services.study_planner import generate_study_plan
from services.rag_tutor import answer_question

from fastapi import UploadFile
from services.pdf_processor import extract_text
from services.vector_store import add_document

router = APIRouter()


class QuizRequest(BaseModel):
    topic: str


class AskRequest(BaseModel):
    question: str


@router.post("/quiz")
def quiz(req: QuizRequest):

    return {
        "quiz":
        generate_quiz(
            req.topic
        )
    }


@router.post("/ask")
def ask(req: AskRequest):

    return {
        "answer":
        answer_question(
            req.question
        )
    }


@router.get("/study-plan")
def planner():

    return {
        "plan":
        generate_study_plan(30, 3, "Machine Learning" )
    }

@router.post("/upload")
async def upload_pdf(file: UploadFile):

    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text(path)

    add_document(text)

    return {
        "message": "Document indexed",
        "length": len(text)
    }


def calculate_accuracy(scores):

    if len(scores) == 0:
        return 0

    return sum(scores) / len(scores)


def weak_topics(progress):

    return [
        p.topic
        for p in progress
            if p.score < 60:
                yield p.topic
    ]