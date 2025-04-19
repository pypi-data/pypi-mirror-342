import google.generativeai as genai
from .pdf_reader import extract_text_from_pdf

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-pro")

def ask_gemini_about_pdf(pdf_path, query, api_key):
    model = init_gemini(api_key)
    context = extract_text_from_pdf(pdf_path)
    prompt = f"""Context from PDF:\n{context[:8000]} \n\nUser Question: {query}"""
    response = model.generate_content(prompt)
    return response.text.strip()
