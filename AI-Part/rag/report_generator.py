def generate_report(llm_client, context):
    """
    Generates a report using the LLM client.
    """
    # Assuming llm_client has a method like generate or __call__
    # Based on main.py: report = generate_report(llm, context)
    # And main.py imports llm from llm_client.
    
    # We will assume llm_client is an object with a .generate(prompt) method 
    # OR we just pass the context to it if it's a function.
    
    # Let's standardize on llm_client.generate(text)
    try:
        response = llm_client.generate(context)
        return response
    except Exception as e:
        return f"Error generating report: {e}"
