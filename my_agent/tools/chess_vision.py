"""
Specialized Chess Vision Tool — Uses Gemini to map pieces, then Python to build the FEN.
"""
import os
import json
from PIL import Image
from google import genai


def extract_chess_fen(image_path: str, turn: str = "b") -> str:
    """Use this tool to extract a precise FEN string from a chessboard image.

    Args:
        image_path: The file path to the chessboard image.
        turn: Whose turn it is. 'w' for white, 'b' for black.

    Returns:
        A valid FEN string to be passed to a chess engine.
    """
    if not os.path.exists(image_path):
        return f"Error: Image not found at {image_path}"

    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)

    # 1. Ask Gemini to just map the coordinates
    prompt = """
    You are a highly precise chess vision system. Look at the provided chessboard image.
    Carefully note the coordinates on the edges. The board in this image is viewed from Black's perspective (rank 8 at the bottom, rank 1 at the top, h-file on the left, a-file on the right).
    
    Identify every piece on the board and its exact algebraic coordinate.
    Use standard piece notation: White = K, Q, R, B, N, P. Black = k, q, r, b, n, p.
    
    Return ONLY a raw JSON dictionary where keys are the square coordinates (e.g., "g1", "d8") and values are the piece letters.
    Example output format:
    {"g1": "K", "h3": "P", "d8": "r"}
    """

    try:
        img = Image.open(image_path)
        # Using the Pro model here is highly recommended for complex spatial reasoning
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[img, prompt],
        )

        # Clean up the JSON if the model added markdown blocks
        json_str = response.text.replace("```json", "").replace("```", "").strip()
        pieces_dict = json.loads(json_str)

        # 2. Use deterministic Python to build the FEN string
        rows = []
        for rank in range(8, 0, -1):  # Loop from rank 8 down to 1
            empty_count = 0
            row_str = ""
            for file_idx in range(8):  # Loop from a to h
                file_char = chr(ord('a') + file_idx)
                square = f"{file_char}{rank}"

                if square in pieces_dict:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    row_str += pieces_dict[square]
                else:
                    empty_count += 1

            if empty_count > 0:
                row_str += str(empty_count)
            rows.append(row_str)

        fen = "/".join(rows) + f" {turn} - - 0 1"
        return fen

    except Exception as e:
        return f"Error extracting FEN: {e}"
