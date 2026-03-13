"""
Image Analysis tool — powered by Gemini 2.5 Flash for high accuracy and low latency.
"""
import os
from PIL import Image
from google import genai

def analyze_image(image_path: str, question: str) -> str:
    """Use this tool to read, analyze, and extract information from image files (like .png or .jpg).

    Always pass the file path of the image and a specific question about what 
    information you need to extract from it. Do not ask for generic descriptions 
    unless explicitly requested by the user.

    Args:
        image_path: The file path to the image (e.g., "benchmark/attachments/14.png").
        question: The specific question to ask about the image content.

    Returns:
        A string containing the answer based on the visual information.
    """
    if not os.path.exists(image_path):
        return f"Error: Image file not found at {image_path}"

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY is not set."

    client = genai.Client(api_key=api_key)

    try:
        # Loading the image into memory with PIL avoids the latency of 
        # a separate File API upload for smaller, local benchmark images.
        img = Image.open(image_path)

        # We use gemini-2.5-flash as it offers the best balance: 
        # lightning-fast latency and exceptional multimodal accuracy.
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, question],
        )
        return response.text.strip()
    except Exception as e:
        return f"Error analyzing image: {e}"