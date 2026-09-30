from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie", version="1.0.0", description="Google Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)

class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)
    count: int = Field(default=3, ge=1, le=10)

class LearningRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=1000)
    level: str = Field(default="Beginner", max_length=50)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}

@app.post("/qa")
async def qa(payload: TextRequest):
    return {"answer": answer_question(payload.text)}

@app.post("/explain")
async def explain(payload: TextRequest):
    return {"answer": explain_topic(payload.text)}

@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        return {"quiz": generate_quiz(payload.text, payload.count)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.post("/summarize")
async def summarize(payload: TextRequest):
    return {"summary": summarize_text(payload.text)}

@app.post("/learn/recommendations")
async def recommendations(payload: LearningRequest):
    return {"recommendations": get_learning_recommendations(payload.topic, payload.level)}
