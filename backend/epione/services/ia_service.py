# epione/services/ia_service.py
from dotenv import load_dotenv
import httpx
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def gerar_raciocinio_clinico(prompt):
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY não está definida no ambiente.")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Você é um médico clínico altamente experiente."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
