import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import FINBERT_MODEL_NAME, FINBERT_BATCH_SIZE


def load_finbert():
    tokenizer = AutoTokenizer.from_pretrained(FINBERT_MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(FINBERT_MODEL_NAME)
    return tokenizer, model


def compute_daily_average_sentiment(tweet_conn, tokenizer, model):
    query = """
        SELECT ts.stock_symbol AS stock, t.text, t.created_at AS date 
        FROM tweets t JOIN tweet_stocks ts ON t.id = ts.tweet_id
    """

    df = pd.read_sql_query(query, tweet_conn)
    texts = df["text"].astype(str).tolist()
    scores = []
    model.eval()
    for i in range(0, len(texts), FINBERT_BATCH_SIZE):
        batch = texts[i : i + FINBERT_BATCH_SIZE]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment = (probs[:, 0] - probs[:, 1]).cpu().numpy()
        scores.extend(sentiment)
    
    df["sentiment"] = scores
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df.groupby(["stock", "date"])["sentiment"].mean().reset_index()