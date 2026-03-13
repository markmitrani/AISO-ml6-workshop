import fitz
import requests
import io


def download_and_read_pdf(url: str, search_term: str = "") -> str:
    """CRITICAL: Use this tool to download and read a PDF from a URL. If a
    search_term is provided, it counts how many pages mention that term.

    Args:
        url: The full URL of the PDF to download.
        search_term: Optional keyword to search for across all pages.

    Returns:
        A string with the keyword count per page, or the first 10,000
        characters of the PDF text if no search_term is given.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        pdf_bytes = io.BytesIO(response.content)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        total_pages = len(doc)

        if search_term:
            count = 0
            search_term_lower = search_term.lower()
            for page in doc:
                text = page.get_text().lower()
                if search_term_lower in text:
                    count += 1
            return f"The term '{search_term}' was found on {count} out of {total_pages} pages in the PDF at {url}."
        else:
            # If no search term, return the first 10000 chars of the document
            full_text = ""
            for page in doc:
                full_text += page.get_text() + "\n"
            return full_text[:10000]

    except Exception as e:
        return f"Error downloading or reading PDF from {url}: {str(e)}"
