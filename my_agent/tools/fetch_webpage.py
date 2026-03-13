"""
Webpage reader tool — powered by Jina Reader API for LLM-optimized Markdown.
"""

import requests


def fetch_webpage(url: str) -> str:
    """Use this tool to read the full content of a specific webpage. Pass the
    exact URL. It will return the page content formatted in clean Markdown.
    Use this if the user provides a URL in their prompt, or if you need more
    details than the web_search snippets provided.

    Args:
        url: The full URL of the webpage to read.

    Returns:
        A string containing the webpage content in clean Markdown format,
        truncated to 100,000 characters, or an error message.
    """
    try:
        jina_url = "https://r.jina.ai/" + url
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; ADKAgent/1.0)"
        }
        response = requests.get(jina_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text[:100000]
    except Exception as e:
        return f"Error fetching webpage: {e}"


def analyze_remote_pdf(url: str, keyword: str) -> str:
    """CRITICAL: Use this tool ONLY if the user provides a URL that ends in
    .pdf, or if you need to read a PDF report from the web. Provide the URL
    and the specific keyword you are looking for (e.g., "nuclear energy").

    Args:
        url: The full URL of the remote PDF file.
        keyword: The specific keyword or phrase to search for in the PDF.

    Returns:
        A string stating how many pages contain the keyword.
    """
    import io

    import pdfplumber

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; ADKAgent/1.0)"
        }
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()

        count = 0
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and keyword.lower() in text.lower():
                    count += 1

        return f"The keyword '{keyword}' appears on {count} pages."
    except Exception as e:
        return f"Error analyzing remote PDF: {e}"
