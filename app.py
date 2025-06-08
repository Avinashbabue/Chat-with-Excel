import os
import google.generativeai as genai

# Try all three model names, one at a time
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Try these, one at a time and comment the rest:
# model = genai.GenerativeModel("models/gemini-pro")
# model = genai.GenerativeModel("gemini-1.0-pro")
model = genai.GenerativeModel("models/gemini-1.5-pro")

try:
    response = model.generate_content("Say hello from Gemini!")
    print("Gemini API test response:", response.text)
    st.success("Gemini API test succeeded: " + response.text)
except Exception as e:
    st.error(f"Gemini API test failed: {e}")
    st.stop()
