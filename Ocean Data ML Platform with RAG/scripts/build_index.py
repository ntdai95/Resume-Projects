from app.rag.runtime import load_docs
from app.retrieval.index_builder import build_index
from app.core.settings import settings


def main():
    build_index(load_docs(), settings.embedding_model)
    print("Built index")


if __name__ == "__main__":
    main()
