from fastapi import APIRouter, Query, Request


router = APIRouter()

@router.get("/search")
def search(request: Request, q: str, top_k: int = Query(default=5, ge=1, le=20)):
    retriever = getattr(request.app.state, "retriever", None)
    if retriever is None:
        return {"results": [], "message": "index not built yet"}

    return {"results": retriever.retrieve(q, top_k=top_k)}