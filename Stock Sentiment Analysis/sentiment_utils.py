import re
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import SENTIMENT_MODEL_NAME, SENTIMENT_BATCH_SIZE


_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_MENTION_RE = re.compile(r"@\w+")
_NONPRINT_RE = re.compile(r"[^\x20-\x7E]+")


def load_sentiment_model():
    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_NAME)
    return tokenizer, model


def clean_tweet_text(s):
    s = s or ""
    s = s.lower()
    s = _URL_RE.sub("", s)
    s = _MENTION_RE.sub("", s)
    s = _NONPRINT_RE.sub(" ", s)
    return " ".join(s.split())


def find_label(keywords, id2label):
    for idx, lab in id2label.items():
        if any(k in lab for k in keywords):
            return idx
            

def compute_daily_average_sentiment(tweet_conn, tokenizer, model):
    query = """
        SELECT
            ts.stock_symbol AS stock,
            t.text,
            t.created_at AS created_at,
            t.lang,
            COALESCE(t.like_count, 0) AS like_count,
            COALESCE(t.retweet_count, 0) AS retweet_count
        FROM tweets t
        JOIN tweet_stocks ts ON t.id = ts.tweet_id
        WHERE t.lang = 'en'
    """

    df = pd.read_sql_query(query, tweet_conn)
    if df.empty:
        return pd.DataFrame(columns=["stock", "date", "sentiment"])

    df["text"] = df["text"].astype(str).map(clean_tweet_text)
    texts = df["text"].tolist()
    model.eval()
    id2label = {int(k): str(v).upper() for k, v in model.config.id2label.items()}
    pos_keywords = ["POS", "BULL"]
    neg_keywords = ["NEG", "BEAR"]
    pos_idx = find_label(pos_keywords, id2label)
    neg_idx = find_label(neg_keywords, id2label)
    if pos_idx is None or neg_idx is None:
        raise RuntimeError(f"Unexpected sentiment labels: {id2label}")

    scores = []
    for i in range(0, len(texts), SENTIMENT_BATCH_SIZE):
        batch = texts[i: i + SENTIMENT_BATCH_SIZE]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment = (probs[:, pos_idx] - probs[:, neg_idx]).detach().cpu().numpy()
        scores.extend(sentiment)

    df["sentiment"] = scores
    df["date"] = pd.to_datetime(df["created_at"]).dt.date
    df["w"] = 1.0 + df["retweet_count"] + 0.5 * df["like_count"]
    daily = (
        df.groupby(["stock", "date"])
          .apply(lambda g: (g["sentiment"] * g["w"]).sum() / g["w"].sum()
                 if g["w"].sum() else g["sentiment"].mean())
          .reset_index(name="sentiment")
    )

    return daily