from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

app = FastAPI()

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable")
openai.api_key = OPENAI_API_KEY

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(msg: Message):
    # Simple pass-through to OpenAI Chat Completion
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg.text}],
            temperature=0.7,
            max_tokens=256,
        )
        answer = resp.choices[0].message.content.strip()
        return {"reply": answer}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"status": "ok", "info": "POST /chat with {text: '...'}"}
