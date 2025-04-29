"""
Optional GPT-3.5/4 integration for advanced data parsing.
"""

import os
import openai
import pandas as pd
from typing import Optional

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def gpt_parse(text: str, prompt_template: Optional[str] = None) -> str:
    """
    Parse text using OpenAI GPT.

    Args:
        text (str): Input text.
        prompt_template (Optional[str]): Prompt template with {text} placeholder.

    Returns:
        str: GPT-parsed structured output.
    """
    if not OPENAI_API_KEY:
        raise EnvironmentError("OpenAI API Key not found. Set OPENAI_API_KEY environment variable.")

    openai.api_key = OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful data parsing assistant."},
                {"role": "user", "content": (prompt_template or "Structure this text: {text}").format(text=text)}
            ],
            temperature=0,
            max_tokens=1000
        )
        return response.choices[0].message["content"].strip()
    
    except Exception as e:
        print(f"[Warning] GPT parsing failed: {e}")
        return text  # fallback to original text
