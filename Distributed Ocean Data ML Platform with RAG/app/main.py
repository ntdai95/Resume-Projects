from contextlib import asynccontextmanager
import torch
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from app.api.routes_ask import router as ask_router
from app.api.routes_eval import router as eval_router
from app.api.routes_forecast import router as forecast_router
from app.api.routes_health import router as health_router
from app.api.routes_metrics import router as metrics_router
from app.api.routes_predict import router as predict_router
from app.api.routes_provenance import router as provenance_router
from app.api.routes_search import router as search_router
from app.core.settings import settings
from app.rag.runtime import ensure_rag_ready


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.ensure_dirs()
    app.state.retriever = None
    app.state.answerer = None
    ensure_rag_ready(app)
    yield


app = FastAPI(title="Ocean ML RAG", lifespan=lifespan)
app.include_router(health_router)
app.include_router(search_router)
app.include_router(ask_router)
app.include_router(provenance_router)
app.include_router(eval_router)
app.include_router(forecast_router)
app.include_router(metrics_router)
app.include_router(predict_router)