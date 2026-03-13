"""
Web search tool — powered by DuckDuckGo Search (DDGS).
"""

from duckduckgo_search import DDGS


def web_search(query: str) -> str:
    """CRITICAL: Use this tool to search the internet for up-to-date facts or
    queries. It returns a list of search results with URLs and snippets. If the
    snippets do not contain the full answer, you MUST use the fetch_webpage tool
    on the most relevant URL.

    Args:
        query: The search query string.

    Returns:
        A formatted string of search results with Title, URL, and snippet for
        each result, or an error message.
    """
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No search results found for: " + query

        output = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            url = r.get("href", "No URL")
            snippet = r.get("body", "No snippet")
            output.append(f"Result {i}:\nTitle: {title}\nURL: {url}\nSnippet: {snippet}\n")

        return "\n".join(output)
    except Exception as e:
        return f"Error performing web search: {e}"
