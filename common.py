import os
import time
import requests
import pandas as pd
from io import StringIO

BASE_DIR = r"D:\NLP\classify"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "gpt-3.5-turbo"


# -------------------------
# File Utilities
# -------------------------

def read_text_file(filename: str) -> str:
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError(f"{filename} is empty")

    return content


def escape_csv(text: str) -> str:
    return text.replace('"', '""')


def save_csv(df: pd.DataFrame, filename: str):
    path = os.path.join(BASE_DIR, filename)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"💾 Saved {filename}")


# -------------------------
# LLM Call
# -------------------------

def call_llm(prompt: str, api_key: str, timeout=20, max_retries=3) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 1500
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=timeout
            )

            if response.status_code == 200:
                text = response.json()["choices"][0]["message"]["content"].strip()
                if text:
                    return text
                print(f"⚠️ Empty response (attempt {attempt})")
            else:
                print(f"⚠️ LLM error {response.status_code}: {response.text}")

        except Exception as e:
            print(f"⚠️ LLM exception: {e}")

        time.sleep(2)

    raise RuntimeError("LLM failed after all retries")