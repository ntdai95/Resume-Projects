from fastapi import APIRouter, HTTPException, Query, Request
from app.rag.evaluation import evaluate_retriever, save_retrieval_eval


router = APIRouter(prefix="/eval", tags=["evaluation"])

@router.post("/retrieval")
def run_retrieval_eval(request: Request, top_k: int = Query(default=5, ge=1, le=20)):
    retriever = getattr(request.app.state, "retriever", None)
    if retriever is None:
        raise HTTPException(status_code=500, detail="Retriever not initialized")

    summary = evaluate_retriever(retriever=retriever, top_k=top_k)
    artifacts = save_retrieval_eval(summary)
    return {
        "message": "Retrieval evaluation completed",
        "metrics": summary["metrics"],
        "num_queries": summary["num_queries"],
        "artifacts": artifacts,
    }