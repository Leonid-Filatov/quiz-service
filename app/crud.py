from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Question
from app.schemas import QuestionCreate
from app.database import SessionLocal
import httpx
import asyncio

async def get_previous_question() -> Question:
    """Получить последний сохраненный вопрос"""
    async with SessionLocal() as db:
        result = await db.execute(
            select(Question).order_by(Question.created_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

async def save_question(question_data: QuestionCreate) -> Question:
    """Сохранить вопрос в базу данных"""
    async with SessionLocal() as db:
        # Проверяем, существует ли уже такой вопрос
        existing = await db.execute(
            select(Question).where(Question.question_id == question_data.question_id)
        )
        if existing.scalar_one_or_none():
            return None
        
        # Создаем новый вопрос
        db_question = Question(
            question_id=question_data.question_id,
            question_text=question_data.question_text,
            answer_text=question_data.answer_text
        )
        db.add(db_question)
        await db.commit()
        await db.refresh(db_question)
        return db_question

async def fetch_questions_from_api(count: int = 1) -> list:
    """Получить вопросы с публичного API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://jservice.io/api/random?count={count}",
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()

async def get_unique_questions(count: int) -> list:
    """Получить уникальные вопросы, которых нет в базе"""
    unique_questions = []
    
    while len(unique_questions) < count:
        # Получаем вопросы из API
        questions_data = await fetch_questions_from_api(count - len(unique_questions))
        
        for question in questions_data:
            question_id = question["id"]
            
            # Проверяем, есть ли такой вопрос в базе
            async with SessionLocal() as db:
                existing = await db.execute(
                    select(Question).where(Question.question_id == question_id)
                )
                if not existing.scalar_one_or_none():
                    # Если вопроса нет в базе, добавляем его
                    unique_questions.append(
                        QuestionCreate(
                            question_id=question_id,
                            question_text=question["question"],
                            answer_text=question["answer"]
                        )
                    )
                    
                    # Если набрали нужное количество, выходим
                    if len(unique_questions) >= count:
                        break
        
        # Чтобы не перегружать API
        if len(unique_questions) < count:
            await asyncio.sleep(0.1)
    
    return unique_questions