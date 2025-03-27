import openai
import json
import os
from typing import Dict, Any
from functools import lru_cache
import re


@lru_cache()
def get_openai_config():
    """
    Gets OpenAI configuration from environment variables.

    Returns:
        Tuple containing API key and model name
    """
    return os.getenv("PLATFORM_OPENAI_KEY"), os.getenv("MODEL_OPENAI")


def extract_important_data(message: str) -> Dict[str, Any]:
    """
    Extracts important data from a message using OpenAI API.

    Args:
        message: The text message to process

    Returns:
        Extracted data as a dictionary
    """
    # Get OpenAI configuration
    api_key, model = get_openai_config()

    # Configure OpenAI
    openai.api_key = api_key

    # Create message for API
    messages = [
        {
            "role": "system",
            "content": "Your responses must always be in JSON format",
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0
    )

    # Get response
    res = response["choices"][0]["message"]["content"]

    # Extract JSON from response
    res_json = re.search(r"```json\s*(.*?)\s*```", res, re.DOTALL)

    # Return JSON
    if res_json:
        return json.loads(res_json.group(1))
    else:
        try:
            return json.loads(res)
        except json.JSONDecodeError:
            return {"error": "GPT não respondeu em formato JSON"}
