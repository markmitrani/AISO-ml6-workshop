"""
Chess Engine tool — powered by Stockfish.
"""
from stockfish import Stockfish

def get_best_chess_move(fen: str) -> str:
    """Use this tool to find the best chess move for a given board position.
    
    Args:
        fen: The Forsyth-Edwards Notation (FEN) string representing the current 
             board state. Make sure the FEN includes whose turn it is 
             (e.g., 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1').
             
    Returns:
        A string containing the best move in algebraic notation.
    """
    try:
        # Initialize Stockfish. It will automatically look for the binary in your PATH.
        stockfish = Stockfish()
        
        # Set the board state using the FEN string
        if not stockfish.is_fen_valid(fen):
            return "Error: Invalid FEN string provided."
            
        stockfish.set_fen_position(fen)
        
        # Get the best move
        best_move = stockfish.get_best_move()
        return f"The best move is {best_move}"
        
    except FileNotFoundError:
        return "Error: Stockfish binary not found. Please install it on your system."
    except Exception as e:
        return f"Error running Stockfish: {e}"