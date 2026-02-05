def build_context(category_df, sample_df):
    
    # Summarize Category Stats
    category_summary = "Category Insights:\n"
    for index, row in category_df.iterrows():
        category_summary += f"- {row['category']}: {row['complaint_count']} complaints, Avg Rating: {row['avg_rating']:.2f}\n"

    # Summarize Sample Complaints
    sample_complaints = "\nRecent Complaints Samples:\n"
    for index, row in sample_df.iterrows():
        sample_complaints += f"- [{row['category']} - {row['sentiment']}] {row['complaint_text']} (Rating: {row['rating']})\n"

    context = f"""
You are an AI assistant analyzing CRM data.
Here is the summary of recent customer complaints:

{category_summary}
{sample_complaints}

Please generate a short executive report summarizing the key issues and suggesting improvements.
"""
    return context
