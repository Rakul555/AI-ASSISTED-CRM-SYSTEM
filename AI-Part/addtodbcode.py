import sys
import os
import pandas as pd
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Database.db_handler import insert_customer_data

def clean_text(text):
    text = str(text).lower()  
    text = re.sub(r"http\S+|www\S+", "", text)   
    text = re.sub(r"[^a-zA-Z\s]", "", text)      
    text = re.sub(r"\s+", " ", text).strip()
    return text


data = pd.read_csv('Dataset/data3.csv', header=0)
data['complaint_text'] = data['complaint_text'].apply(lambda x: clean_text(x))

for i in range(len(data)):
    text = str(data['complaint_text'][i])
    category = str(data['category'][i])
    sentiment = str(data['sentiment'][i])
    rating = int(data['rating'][i])          
    confidence = float(data['confidence'][i]) 
    insert_customer_data(text, category, sentiment, rating, confidence)

print("Success")