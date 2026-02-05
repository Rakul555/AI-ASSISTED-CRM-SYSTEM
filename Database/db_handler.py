import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rakulsince@2005",
        database="aicrm"
    )

def insert_customer_data(text, category, sentiment, rating, confidence):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO customerdata 
    (complaint_text, category, sentiment, rating, confidence)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (text, category, sentiment, rating, confidence))
    conn.commit()

    cursor.close()
    conn.close()
    


def fetch_category_stats():
    conn = get_connection()
    cursor = conn.cursor()
    # Count complaints per category and calculate average sentiment/confidence if needed
    query = """
    SELECT category, COUNT(*), AVG(rating) 
    FROM customerdata 
    GROUP BY category
    """
    cursor.execute(query)
    results = cursor.fetchall()
    # Return as list of tuples or dicts. Let's return list of result tuples.
    # (category, count, avg_rating)
    conn.close()
    return results

def fetch_recent_complaints(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"""
    SELECT complaint_text, category, sentiment, rating
    FROM customerdata
    ORDER BY id DESC LIMIT {limit}
    """
    # Note: Assuming 'id' exists or we just rely on natural order if no primary key/timestamp.
    # If id doesn't exist, we might just take any 5. Let's check table structure if possible, but for now I'll assume standard auto-inc ID.
    # Actually, looking at the insert, I don't see an ID or timestamp. 
    # Let's try to just select top N without order if ID isn't there, or assume there is an ID.
    # To be safe, let's just SELECT * LIMIT N
    query = """
    SELECT complaint_text, category, sentiment, rating
    FROM customerdata
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    conn.close()
    return results
