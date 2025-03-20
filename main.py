from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI app
app = FastAPI()

# Request model
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Welcome!"}

@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.message}]
        )

        # Extract response
        bot_reply = response.choices[0].message.content
        return {"reply": bot_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
