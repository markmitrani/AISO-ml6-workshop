"""
Webpage reader tool — powered by Jina Reader API for LLM-optimized Markdown.
"""

import requests


def fetch_webpage(url: str) -> str:
    """CRITICAL: Use this tool to read the full content of a specific webpage.
    Pass the exact URL. It will return the page content formatted in clean
    Markdown.

    Args:
        url: The full URL of the webpage to read.

    Returns:
        A string containing the webpage content in clean Markdown format,
        truncated to 100,000 characters, or an error message.
    """
    try:
        jina_url = "https://r.jina.ai/" + url
        response = requests.get(jina_url, timeout=30)
        response.raise_for_status()
        return response.text[:100000]
    except Exception as e:
        return f"Error fetching webpage: {e}"
