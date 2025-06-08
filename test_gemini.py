import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-pro")  # Try this, or "gemini-1.0-pro"
response = model.generate_content("Say hello.")
print(response.text)
