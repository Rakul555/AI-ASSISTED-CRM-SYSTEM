import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RAG.retriever import fetch_category_insights, fetch_sample_complaints
from RAG.context_builder import build_context
from RAG.report_generator import generate_report

from llm_client import llm  

def run_rag():
    category_df = fetch_category_insights()
    sample_df = fetch_sample_complaints()

    context = build_context(category_df, sample_df)
    report = generate_report(llm, context)

    print("\n===== GENERATED REPORT =====\n")
    print(report)

if __name__ == "__main__":
    run_rag()