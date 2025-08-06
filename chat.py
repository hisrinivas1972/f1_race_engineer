import google.generativeai as genai
import os

def setup_gemini(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-pro")

def ask_strategy(model, prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
