"""
Image analysis tool — powered by Gemini's multimodal vision API.
"""

import base64
import os

from google import genai


def analyze_image(image_path: str, question: str) -> str:
    """CRITICAL: Use this tool whenever the user mentions an attached image
    file (e.g., a .png, .jpg, or .jpeg file). Provide the file path and the
    full question text. The tool uses Gemini's vision capabilities to analyze
    the image and answer the question about it.

    Args:
        image_path: The absolute or relative path to the image file.
        question: The full question to answer about the image.

    Returns:
        A string containing Gemini's analysis of the image.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY is not set."

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    except FileNotFoundError:
        return f"Error: Image file not found at '{image_path}'."
    except Exception as e:
        return f"Error reading image file: {e}"

    # Determine MIME type from extension
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime_type = mime_map.get(ext, "image/png")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": question},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": base64.standard_b64encode(image_bytes).decode("utf-8"),
                            }
                        },
                    ],
                }
            ],
        )
        return response.text.strip()
    except Exception as e:
        return f"Error analyzing image: {e}"
