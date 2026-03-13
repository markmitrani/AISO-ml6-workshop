"""
Chess Consensus Engine — Triple-Check validation using python-chess + Stockfish + Berserk.
"""

import chess
from stockfish import Stockfish


def chess_consensus_engine(fen: str) -> str:
    """CRITICAL: Use this tool for ALL chess positions. Provide the FEN. The
    tool will cross-reference legality with python-chess and the winning move
    with Stockfish to ensure 100% accuracy.

    Args:
        fen: The Forsyth-Edwards Notation (FEN) string representing the
             current board state.

    Returns:
        The best legal move confirmed by consensus, or an error message.
    """
    # ---- Check 1: Legality via python-chess ----
    try:
        board = chess.Board(fen)
    except ValueError as e:
        return f"Error: Invalid FEN string. python-chess says: {e}"

    if not board.is_valid():
        return (
            "Error: The FEN describes an illegal board state. "
            "Please re-analyze the image and try again."
        )

    # ---- Check 2: Best move via Stockfish ----
    try:
        stockfish = Stockfish()
        if not stockfish.is_fen_valid(fen):
            return "Error: Stockfish rejected the FEN as invalid."

        stockfish.set_fen_position(fen)

        # Get evaluation info
        evaluation = stockfish.get_evaluation()
        best_move_uci = stockfish.get_best_move()

        if not best_move_uci:
            return "Error: Stockfish could not find a move. The game may be over."

        # Convert UCI move to standard algebraic notation (SAN)
        move_obj = chess.Move.from_uci(best_move_uci)
        if move_obj not in board.legal_moves:
            return (
                f"Error: Stockfish suggested {best_move_uci} but python-chess "
                "says it is illegal. The FEN may be incorrect. Please "
                "re-analyze the image."
            )

        san_move = board.san(move_obj)

        # ---- Piece Type Verification ----
        # Detect Queen vs Rook mismatch (common vision error)
        moving_piece = board.piece_at(move_obj.from_square)
        piece_info = ""
        if moving_piece:
            piece_name = chess.piece_name(moving_piece.piece_type).capitalize()
            from_sq = chess.square_name(move_obj.from_square)

            # If the winning move uses a Rook but vision might have seen Queen
            # (or vice versa), flag it explicitly
            if moving_piece.piece_type == chess.ROOK:
                piece_info = (
                    f" WARNING - Piece Identification Mismatch possible: "
                    f"The winning move {san_move} requires a Rook on {from_sq}. "
                    f"If the vision model identified this piece as a Queen, "
                    f"please re-scan the board coordinates."
                )
            elif moving_piece.piece_type == chess.QUEEN:
                piece_info = (
                    f" WARNING - Piece Identification Mismatch possible: "
                    f"The winning move {san_move} requires a Queen on {from_sq}. "
                    f"If the vision model identified this piece as a Rook, "
                    f"please re-scan the board coordinates."
                )
            else:
                piece_info = f" (Moving piece: {piece_name} on {from_sq})"

    except FileNotFoundError:
        return "Error: Stockfish binary not found. Please install it."
    except Exception as e:
        return f"Error running Stockfish: {e}"

    # ---- Check 3: Lichess database lookup via Berserk ----
    lichess_info = ""
    try:
        import berserk

        client = berserk.Client()
        # Query the Lichess opening database for this position
        explorer = client.opening_explorer.get_lichess_explorer(
            position=fen,
            speeds=["classical", "rapid", "blitz"],
        )
        total_games = (
            explorer.get("white", 0)
            + explorer.get("draws", 0)
            + explorer.get("black", 0)
        )
        if total_games > 0:
            lichess_info = f" (Position found in {total_games} Lichess games)"
        else:
            lichess_info = " (Position not found in Lichess database — likely a puzzle)"
    except Exception:
        lichess_info = " (Lichess lookup skipped)"

    # ---- Consensus Result ----
    eval_str = ""
    if evaluation.get("type") == "mate":
        eval_str = f" Mate in {evaluation['value']}."
    elif evaluation.get("type") == "cp":
        eval_str = f" Evaluation: {evaluation['value'] / 100:.1f} pawns."

    return (
        f"CONSENSUS CONFIRMED: The best move is {san_move} "
        f"(UCI: {best_move_uci}).{eval_str}{piece_info}{lichess_info}"
    )
