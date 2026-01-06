from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "backend running"}

@app.post("/ask")
def ask_ai(q: Question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior data engineer."},
            {"role": "user", "content": q.question}
        ],
        temperature=0.3,
        max_tokens=300
    )

    return {
        "answer": response.choices[0].message.content.strip()
    }
