import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_APIKEY"))
model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content("")
print(response.text.replace('#','').replace('*',''))