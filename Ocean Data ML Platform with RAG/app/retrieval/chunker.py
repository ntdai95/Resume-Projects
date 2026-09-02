def chunk_text(text, chunk_size=600, chunk_overlap=100):
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start += max(1, chunk_size - chunk_overlap)
        
    return chunks
