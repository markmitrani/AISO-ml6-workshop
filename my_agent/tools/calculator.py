"""
Universal Math Solver tool — powered by Gemini (parsing) + SymPy (evaluation).
"""

import os

from google import genai
from sympy import sympify
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


def universal_math_solver(math_query: str) -> str:
    """Use this tool for ALL math, arithmetic, algebra, or calculus questions.

    Pass the entire unstructured math question as the 'math_query' string
    argument. Do NOT attempt to solve math yourself — always delegate to this
    tool.  It handles addition, subtraction, multiplication, division,
    exponentiation, roots, integrals, derivatives, equation solving, rounding,
    and any other mathematical operation.

    Args:
        math_query: The full, unstructured math question in natural language
                    (e.g. "What is 2 raised to the power of 47 divided by 378?").

    Returns:
        A string containing the computed numerical or symbolic answer.
    """

    # --- Step 1: Use Gemini to parse the natural-language query into SymPy ---
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY is not set."

    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are a parsing engine. Convert the following unstructured math "
        "question into a strictly valid, single-line SymPy-compatible "
        "mathematical expression string.\n"
        "Rules:\n"
        "- Use Python/SymPy syntax: ** for power, sqrt() for square root, "
        "Rational() for exact fractions, integrate(expr, x), diff(expr, x), "
        "solve(Eq(lhs, rhs), x), etc.\n"
        "- If the question asks to round the result, wrap the expression with "
        "round(<expr>, <decimals>).\n"
        "- If the question asks for the square root of an answer, compute the "
        "inner expression first inside sqrt(), e.g. sqrt(347.8 * 219.6).\n"
        "- Output ONLY the raw expression string. No markdown, no backticks, "
        "no explanations, no extra text.\n"
        "Examples:\n"
        "  'What is 4782969 divided by 127 rounded to 2 decimal places?' "
        "-> round(4782969 / 127, 2)\n"
        "  'What is 2 raised to the power of 47 divided by 378?' "
        "-> 2**47 / 378\n"
        "  'Area of 347.8 by 219.6, give the square root' "
        "-> sqrt(347.8 * 219.6)\n"
        "  'integrate x squared' -> integrate(x**2, x)\n"
        "  'solve 2x + 5 = 15' -> solve(Eq(2*x + 5, 15), x)\n"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=math_query,
            config={"system_instruction": system_instruction},
        )
        sympy_expr_str = response.text.strip()
    except Exception as e:
        return f"Error calling Gemini for parsing: {e}"

    # Clean up any markdown backticks that Gemini might sneak in
    sympy_expr_str = sympy_expr_str.replace("```python", "").replace("```", "").strip()

    # --- Step 2: Evaluate using SymPy ---
    try:
        # Handle the round() wrapper specially since it's a Python builtin,
        # not a SymPy function.
        if sympy_expr_str.startswith("round("):
            result = eval(
                sympy_expr_str,
                {"__builtins__": {}},
                {
                    "round": round,
                    "sqrt": lambda x: float(sympify(f"sqrt({x})")),
                    "Rational": lambda a, b=1: a / b,
                },
            )
            return str(result)

        # Standard SymPy parse with implicit multiplication and xor conversion
        transformations = standard_transformations + (
            implicit_multiplication_application,
            convert_xor,
        )
        result = parse_expr(sympy_expr_str, transformations=transformations)

        # Evaluate to a float if it's numeric
        evaluated = result.evalf()
        float_val = float(evaluated)

        # Return a clean number: remove trailing zeros for integers
        if float_val == int(float_val) and "." not in sympy_expr_str:
            return str(int(float_val))
        # Use explicit rounding for currency/decimal answers
        return str(round(float_val, 2))

    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        # Fallback: try sympify directly
        try:
            result = sympify(sympy_expr_str)
            evaluated = result.evalf()
            return str(round(float(evaluated), 2))
        except Exception:
            return f"Error evaluating expression '{sympy_expr_str}': {e}"
