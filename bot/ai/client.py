# client.py
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

client = Together(api_key=TOGETHER_API_KEY)

def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": prompt}]
        )
        if response and response.choices:
            return response.choices[0].message.content.strip()
        return "Error: No response from API."
    except Exception as e:
        return f"Error: {str(e)}"