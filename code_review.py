import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash-lite')

def analyze_code(code: str) -> str:
    if not code.strip():
        return "No code provided."

    prompt = f"""
You are an expert AI code reviewer. Review the following code and provide:
1. Summary of the code
2. Code quality analysis
3. Suggestions for improvement
4. Potential bugs
5. A rating out of 10

Code:
\\```python
{code}
\\```
"""
    response = model.generate_content(prompt)
    return response.text.strip()


def fix_code(code: str) -> str:
    if not code.strip():
        return "No code provided to fix."

    prompt = f"""
You are an AI coding assistant. Fix the following code for any bugs, bad practices, and improve its readability. 
Only return the corrected code without explanation, formatted as plain code.

Code:
\\```python
{code}
\\```
"""
    response = model.generate_content(prompt)
    return response.text.strip()