import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_recipe_suggestion(ingredients: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional chef who creates structured recipes."
                },
                {
                    "role": "user",
                    "content": f"""
Create a detailed recipe using:
{ingredients}

Format:
Recipe Name:
Ingredients:
Instructions:
"""
                }
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)
        return "Error generating recipe"