import pandas as pd
from Database.db_handler import fetch_category_stats, fetch_recent_complaints

def fetch_category_insights():
    results = fetch_category_stats()
    # results is list of (category, count, avg_rating)
    df = pd.DataFrame(results, columns=['category', 'complaint_count', 'avg_rating'])
    return df

def fetch_sample_complaints():
    results = fetch_recent_complaints(limit=5)
    # results is list of (text, category, sentiment, rating)
    df = pd.DataFrame(results, columns=['complaint_text', 'category', 'sentiment', 'rating'])
    return df
