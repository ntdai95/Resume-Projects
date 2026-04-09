from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field


router = APIRouter()

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/ask")
def ask(request: Request, payload: AskRequest):
    answerer = getattr(request.app.state, "answerer", None)
    if answerer is None:
        raise HTTPException(status_code=500, detail="LLM answerer not initialized")

    return answerer.answer(payload.question, top_k=payload.top_k)