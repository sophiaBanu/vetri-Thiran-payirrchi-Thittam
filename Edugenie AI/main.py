from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class TaskRequest(BaseModel):
    task: Literal[
        "qa",
        "explain",
        "quiz",
        "summarize",
        "learn"
    ] = "qa"

    text: str = Field(
        min_length=1,
        max_length=12000
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.post("/qa")
async def qa(payload: TaskRequest):
    result = answer_question(payload.text)
    return {"result": result}


@app.post("/explain")
async def explain(payload: TaskRequest):
    result = explain_topic(payload.text)
    return {"result": result}


@app.post("/quiz")
async def quiz(payload: TaskRequest):
    result = generate_quiz(payload.text)
    return {"result": result}


@app.post("/summarize")
async def summarize(payload: TaskRequest):
    result = summarize_text(payload.text)
    return {"result": result}


@app.post("/learn/recommendations")
async def learning_recommendations(payload: TaskRequest):
    result = get_learning_recommendations(payload.text)
    return {"result": result}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }