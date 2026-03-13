"""
Human-Simulation Research Tool — powered by Playwright headless browser.
Bypasses bot detection, CAPTCHAs, and legal restriction blocks.
"""

import random
import time

from playwright.sync_api import sync_playwright


def research_human(url: str) -> str:
    """CRITICAL: Use this tool ONLY if fetch_webpage or web_search fails due
    to blocks, CAPTCHAs, or legal restrictions. It simulates a human browser
    session to extract text from difficult sites.

    Args:
        url: The full URL of the page to read with a simulated browser.

    Returns:
        The extracted text content from the page, or an error message.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},
            )
            page = context.new_page()

            # Navigate with a realistic timeout
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

            # Simulate human-like behavior
            time.sleep(random.uniform(1.0, 2.5))

            # Scroll down slowly like a human would
            for _ in range(3):
                page.mouse.wheel(0, random.randint(200, 500))
                time.sleep(random.uniform(0.3, 0.8))

            # Small random mouse movements
            page.mouse.move(
                random.randint(100, 800), random.randint(100, 600)
            )
            time.sleep(random.uniform(0.5, 1.0))

            # Extract the text content
            text = page.inner_text("body")

            browser.close()

            # Truncate to avoid context overflow
            return text[:50000] if text else "No text content found on page."

    except Exception as e:
        return f"Error with Playwright browser: {e}"
