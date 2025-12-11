from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class QuizRequest(BaseModel):
    questions_num: int = Field(
        gt=0, 
        le=100, 
        description="Number of questions to fetch (1-100)"
    )

class QuestionResponse(BaseModel):
    id: Optional[int] = None
    question_text: Optional[str] = None
    answer_text: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    question_id: int
    question_text: str
    answer_text: str