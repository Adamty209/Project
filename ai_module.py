# ai_module.py
from openai import OpenAI
import os

# Set up the OpenAI client (use the API key from environment variables)
client = OpenAI()

def get_npc_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "..."
