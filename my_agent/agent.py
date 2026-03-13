"""
This file is where you will implement your agent.
The `root_agent` is used to evaluate your agent's performance.
"""

from google.adk.agents import llm_agent

from my_agent.tools import (
    extract_pdf_text,
    fetch_webpage,
    universal_math_solver,
    web_search,
)

root_agent = llm_agent.Agent(
    model="gemini-2.5-flash",
    name="agent",
    description="A helpful assistant with access to a powerful math solver.",
    instruction=(
        "You are a helpful assistant that answers questions directly and "
        "concisely.\n\n"
        "You have access to a universal_math_solver tool. Use this tool for "
        "ALL arithmetic, equations, and math-related questions. Do not attempt "
        "to do math in your head; always defer to the solver. Pass the entire "
        "unstructured math question as the 'math_query' argument.\n\n"
        "After receiving the tool's result, return ONLY the final numerical "
        "answer with no extra words, units, or explanation unless the question "
        "specifically asks for them.\n\n"
        "If a question references an attached file or a PDF, you MUST use the "
        "extract_pdf_text tool to read its contents before answering. The file "
        "path will usually be provided in the prompt context.\n\n"
        "CRITICAL: You have full access to the internet via your tools. If asked "
        "about external facts, historical data, or a DOI/URL, you MUST first use "
        "web_search. Then, you MUST IMMEDIATELY use the fetch_webpage tool on "
        "the most promising URL from the search results to read its full HTML body. "
        "NEVER attempt to answer based only on short search snippets. If the first "
        "fetched page doesn't have the answer, fetch the next URL. NEVER say "
        "you cannot access URLs."
    ),
    tools=[universal_math_solver, extract_pdf_text, web_search, fetch_webpage],
    sub_agents=[],
)
