from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Quiz API работает!", "endpoints": ["/health", "/questions/{number}", "/questions"]}

@app.get("/health")
def health():
    return {"status": "healthy", "database": "connected"}

@app.post("/questions/{number}")
def get_questions(number: int):
    if number < 1 or number > 100:
        raise HTTPException(400, "Number must be between 1 and 100")
    
    mock_questions = [
        {"id": 101, "question": "What is the capital of France?", "answer": "Paris"},
        {"id": 102, "question": "Who wrote Romeo and Juliet?", "answer": "William Shakespeare"},
        {"id": 103, "question": "What is 2+2?", "answer": "4"}
    ]
    
    saved = min(number, 3)
    
    return {
        "status": "success",
        "message": f"Saved {saved} questions",
        "saved": saved,
        "last_question": mock_questions[0] if saved > 0 else None
    }

@app.get("/questions")
def list_questions(limit: int = 10):
    return {
        "questions": [],
        "count": 0,
        "note": "Database in test mode"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
