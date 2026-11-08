def format_context(results):
    return [f"Dataset: {r.get('dataset_id')}\nSource file: {r.get('source_file')}\nText: {r.get('text','')}" for r in results]
