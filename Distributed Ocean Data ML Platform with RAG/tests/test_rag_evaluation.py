from app.rag.evaluation import RetrievalEvalExample, evaluate_retriever


class DummyRetriever:
    def retrieve(self, query, top_k=2):
        mapping = {
            "Which datasets contain sea water temperature?": [
                {
                    "doc_id": "doc1",
                    "dataset_id": "onc_temperature",
                    "text": "Dataset onc_temperature includes sea water temperature observations.",
                }
            ],
            "Which datasets mention salinity?": [
                {
                    "doc_id": "doc2",
                    "dataset_id": "onc_salinity",
                    "text": "Dataset onc_salinity contains salinity measurements.",
                }
            ],
        }

        return mapping.get(query, [])


def test_retrieval_eval_summary():
    retriever = DummyRetriever()
    examples = [
        RetrievalEvalExample(
            question="Which datasets contain sea water temperature?",
            relevant_terms=["sea water temperature", "temperature"],
        ),
        RetrievalEvalExample(
            question="Which datasets mention salinity?",
            relevant_terms=["salinity"],
        ),
    ]

    summary = evaluate_retriever(retriever, examples=examples, top_k=2)
    assert summary["num_queries"] == 2
    assert summary["metrics"]["hit_at_k"] == 1.0
    assert summary["metrics"]["term_recall"] > 0.5