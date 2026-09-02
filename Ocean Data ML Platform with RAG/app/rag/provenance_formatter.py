def format_context(results):
    return [f"Dataset: {r['metadata'].get('dataset_id')}\nSource file: {r['metadata'].get('source_file')}\nText: {r['metadata'].get('text','')}" for r in results]
