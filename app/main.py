from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.rag import get_relevant_chunks
from typing import Optional
import uvicorn

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # Optional base64 image (not used here)

@app.post("/api/")
async def answer_question(request: QuestionRequest):
    try:
        relevant_chunks = get_relevant_chunks(request.question)
        context = "\n\n".join(relevant_chunks)

        # Simple logic: just return the top chunks as "answer"
        answer = f"Answer based on course content:\n{context[:1000]}..."  # truncate for demo
        return {
            "answer": answer,
            "links": []  # Static structure for promptfoo compatibility
        }
    except Exception as e:
        return {
            "answer": f"Error generating answer: {str(e)}",
            "links": []
        }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
