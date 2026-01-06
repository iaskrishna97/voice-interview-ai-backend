from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Question(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "backend running"}

@app.post("/ask")
def ask_ai(q: Question):
    if not OPENAI_API_KEY:
        return {"answer": "❌ OpenAI API key not found"}

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a senior data engineer."},
                    {"role": "user", "content": q.question}
                ],
                "temperature": 0.3,
                "max_tokens": 300
            },
            timeout=20
        )

        data = response.json()

        if "choices" not in data:
            return {"answer": f"❌ OpenAI error: {data}"}

        return {
            "answer": data["choices"][0]["message"]["content"].strip()
        }

    except Exception as e:
        return {"answer": f"❌ Backend exception: {str(e)}"}
