"""
Web search tool — powered by DuckDuckGo Search (DDGS).
"""

from duckduckgo_search import DDGS


def web_search(query: str) -> str:
    """CRITICAL: Use this tool to search the internet for up-to-date facts,
    historical data, or general queries. Pass a highly targeted search query
    string. It returns a list of search results with URLs and snippets. If the
    snippets do not contain the full answer, you MUST use the fetch_webpage
    tool on the most relevant URL.

    Args:
        query: The search query string.

    Returns:
        A formatted string of search results with Title, URL, and snippet for
        each result, or an error message.
    """
    try:
        results = DDGS().text(query, max_results=8)

        if not results:
            return (
                "Search returned no results due to rate limits. You MUST guess "
                "the direct URL (like a Wikipedia page) and use fetch_webpage instead."
            )

        formatted = []
        for r in results:
            formatted.append(
                f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n---"
            )
        return "\n".join(formatted)
    except Exception as e:
        return f"Search failed with error: {str(e)}. Try a different query."
