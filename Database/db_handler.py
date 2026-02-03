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
    
value=get_connection()
cursor=value.cursor()
cursor.execute("SELECT * FROM customerdata")
print(cursor.fetchall())
