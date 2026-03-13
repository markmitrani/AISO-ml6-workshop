import math


def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result as a string.

    Use this tool for ANY numerical computation — never perform arithmetic mentally.
    Supports standard operators (+, -, *, /), exponentiation (**), and all Python
    math module functions (math.sqrt, math.floor, math.ceil, math.log, etc.).

    Call this tool once per sub-calculation, chaining results across multiple calls
    when a problem has multiple steps. Always respect order of operations.

    Examples:
        calculator("4782969 / 127")                   -> "37661.1732..."
        calculator("2**47 / 378")                     -> "372321397765.41797"
        calculator("math.sqrt(347.8 * 219.6)")        -> "276.36..."
        calculator("round(4782969 / 127, 2)")         -> "37661.17"
        calculator("(100 + 200) * 1.5 / 60")          -> "7.5"

    Args:
        expression: A valid Python math expression string.

    Returns:
        The result of the expression as a string.
    """
    safe_globals = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    safe_globals["abs"] = abs
    safe_globals["round"] = round
    safe_globals["int"] = int
    safe_globals["float"] = float

    try:
        result = eval(expression, {"__builtins__": {}}, safe_globals)  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Error evaluating expression '{expression}': {e}"
