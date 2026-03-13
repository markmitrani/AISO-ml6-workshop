import base64
import mimetypes
import os
import pathlib

from google import genai
from google.genai import types


def analyze_image(file_path: str, question: str = "") -> str:
    """
    Analyze an image file and return a detailed description or answer to a question about it.

    Use this tool whenever the question references an image file (e.g. a .png or .jpg).
    The file_path is the exact path provided in the 'Note: The following files are relevant' message.

    This tool is required for:
    - Reading text, tables, or pricing information from screenshots
    - Grading or interpreting handwritten or printed worksheets
    - Analyzing chess board positions or other diagrams

    Args:
        file_path: Path to the image file (absolute or relative to the working directory).
        question: A specific question to answer about the image. If empty, returns a
                  detailed description of the image contents.

    Returns:
        A text answer or description of the image contents.

    Examples:
        analyze_image("benchmark/attachments/14.png",
                      "List all storage plans showing their name, price, and storage limit.")
        analyze_image("benchmark/attachments/15.png",
                      "List each problem number, what operation it tests, and whether the student's answer is correct.")
        analyze_image("benchmark/attachments/16.png",
                      "It is black's turn. What single move guarantees a win? Respond in algebraic notation only.")
    """
    path = pathlib.Path(file_path)
    if not path.is_absolute():
        path = pathlib.Path(os.getcwd()) / path

    if not path.exists():
        return f"Error: file not found at {path}"

    mime_type, _ = mimetypes.guess_type(str(path))
    if mime_type is None:
        mime_type = "image/png"

    image_bytes = path.read_bytes()
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    prompt = question if question.strip() else "Describe the contents of this image in detail."

    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            types.Part.from_text(text=prompt),
        ],
    )

    return response.text
