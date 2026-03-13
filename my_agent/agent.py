"""
This file is where you will implement your agent.
The `root_agent` is used to evaluate your agent's performance.
"""

from google.adk.agents import llm_agent

from my_agent.tools import analyze_image, calculator

root_agent = llm_agent.Agent(
    model="gemini-2.5-flash",
    name="agent",
    description="A helpful assistant that reasons carefully and uses tools for precise computation.",
    instruction=(
        "You are a precise and methodical assistant. Follow these rules:\n\n"
        "1. META-INSTRUCTIONS FIRST: If the question contains explicit instructions "
        "about what to write (e.g. 'write only X'), follow them literally — skip "
        "all reasoning and output exactly what is asked.\n\n"
        "2. IMAGES: When a .png or .jpg file path is mentioned in the question, "
        "you MUST call analyze_image with that file path and a specific question "
        "about what you need to know. Never answer image questions without calling "
        "this tool first.\n\n"
        "3. CALCULATOR: Use the calculator tool for ALL arithmetic — never compute "
        "numbers in your head. Use explicit parentheses. Call it once per sub-step "
        "for multi-step problems.\n\n"
        "4. MULTI-STEP PROBLEMS: Think step by step. Gather all information first "
        "(via tools), then compute, then state the answer.\n\n"
        "5. ANSWER FORMAT: Output only what is asked. Show reasoning and tool "
        "results, then state the final answer on its own last line."
    ),
    tools=[calculator, analyze_image],
    sub_agents=[],
)
