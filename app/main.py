from fastapi import FastAPI, HTTPException
from app.database import engine, Base
from app.models import Question
from app.schemas import QuizRequest, QuestionResponse
from app.crud import get_previous_question, save_question, get_unique_questions
import httpx
import asyncio

app = FastAPI(title="Quiz Service API")

# Создаем таблицы в базе данных
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {
        "message": "Quiz Service is running!",
        "docs": "Go to /docs for API documentation",
        "version": "1.0.0"
    }

@app.post("/quiz/", response_model=QuestionResponse)
async def get_quiz_questions(quiz_request: QuizRequest):
    """
    Получить вопросы для викторины.
    
    - **questions_num**: количество вопросов для получения
    """
    questions_num = quiz_request.questions_num
    
    if questions_num <= 0:
        raise HTTPException(
            status_code=400, 
            detail="Number of questions must be positive"
        )
    
    # Получаем предыдущий вопрос
    previous_question = await get_previous_question()
    
    # Получаем уникальные вопросы
    questions = await get_unique_questions(questions_num)
    
    # Сохраняем вопросы в базу данных
    for question_data in questions:
        await save_question(question_data)
    
    # Возвращаем предыдущий вопрос или пустой объект
    if previous_question:
        return QuestionResponse(
            id=previous_question.id,
            question_text=previous_question.question_text,
            answer_text=previous_question.answer_text,
            created_at=previous_question.created_at
        )
    return QuestionResponse()