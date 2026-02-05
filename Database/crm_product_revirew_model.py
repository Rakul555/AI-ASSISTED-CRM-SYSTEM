import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformers import pipeline
import re
from db_handler import insert_customer_data


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)   
    text = re.sub(r"[^a-zA-Z\s]", "", text)      
    text = re.sub(r"\s+", " ", text).strip()
    return text

#==================================================================================================================

#                                             Complaint Classification Model

#==================================================================================================================


COMPLAINT_LABEL_MAPPING = {

    # 🔹 Delivery Issues
    "Late delivery or delayed shipment": "Delivery Issues",
    "Package not delivered or missing shipment": "Delivery Issues",
    "Incorrect delivery address or courier problem": "Delivery Issues",

    # 🔹 Billing & Payment Issues
    "Incorrect billing or extra charges applied": "Billing Issues",
    "Payment deducted but order not confirmed": "Billing Issues",
    "Refund amount not credited after payment failure": "Billing Issues",

    # 🔹 Customer Service Issues
    "Poor customer service or unresponsive support": "Customer Service Issues",
    "Customer support did not resolve the issue": "Customer Service Issues",
    "Rude or unprofessional customer service experience": "Customer Service Issues",

    # 🔹 Product Quality Issues
    "Damaged or defective product received": "Product Quality Issues",
    "Poor material quality or broken product parts": "Product Quality Issues",
    "Product not matching the description provided": "Product Quality Issues",

    # 🔹 Refund & Return Issues
    "Refund delayed or not processed after return": "Refund & Return Issues",
    "Return request rejected or delayed": "Refund & Return Issues",
    "Warranty claim not honored by the seller": "Refund & Return Issues",

    # 🔹 Technical / App Issues
    "Mobile app crashing or not working properly": "Technical Issues",
    "Website payment or checkout failure": "Technical Issues",
    "Technical error while placing the order": "Technical Issues"
}

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)


def classify_text(text, labels, threshold=0.4):
    text = clean_text(text)

    if len(text.split()) < 5:
        return "Unclear feedback", 0.0

    result = classifier(
        text,
        labels,
        hypothesis_template=hypothesis_template,
        multi_label=False
    )

    label = result["labels"][0]
    score = result["scores"][0]

    if score < threshold:
        return "Other / Uncertain", score

    return label, score

hypothesis_template = "This customer feedback is about {}."




#==================================================================================================================

#                                             Sentiment Analysis Model

#==================================================================================================================

classifier2 = pipeline("zero-shot-classification",
                      model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
                      device=0)

candidate_labels = ["Best", "Good", "Average", "Fair", "Bad"]
dict1={"Best":5,"Good":4,"Average":3,"Fair":2,"Bad":1}

def sentiment_analysis(text):
    text = clean_text(text)
    if len(text.split()) < 5:
        return "Unclear feedback", 0.0
    
    result = classifier2(text, candidate_labels)
    label = result["labels"][0]
    score = result["scores"][0]
    
    if score < 0.5:
        return "Other / Uncertain", score
    
    return label, score

#--------------------------------------------------------------------------------------------------------------
    
# classifier2 = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
reviews = """I purchased the OmniStream 4K Pro hub last month hoping it would solve my connectivity problems, but it has been a nightmare of technical glitches from day one. 
Initially, the installation process was smooth, but as soon as I tried to bridge it with my existing mesh network, the device started power cycling randomly. 
I checked the event logs, and it keeps throwing a 'Error 505: Gateway Timeout' every time I attempt a firmware update. 
I’ve tried resetting it to factory settings three times, changing the DNS configuration, and even swapping out the CAT6 cables, but the packet loss is still sitting at around 15% during peak hours. To make matters worse, the companion app crashes on Android 14 whenever I try to access the advanced settings to toggle the firewall. This isn't just a user error; there is clearly a bug in the latest patch that conflicts with legacy router protocols. I need a developer to look at my logs or I need a full refund because this hardware is currently serving as an expensive paperweight.
"""

sentiment, score = sentiment_analysis(reviews)
label, confidence = classify_text(reviews, list(COMPLAINT_LABEL_MAPPING.keys()))

print("Predicted Label:", COMPLAINT_LABEL_MAPPING[label])
print("Confidence Score:", confidence)

print("Predicted Label:", sentiment)
print("Confidence Score:", score)

insert_customer_data(reviews, COMPLAINT_LABEL_MAPPING[label], sentiment, dict1[sentiment], confidence)