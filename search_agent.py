"""
search_agent
This code creates an AI “search agent” whose job is:
    - Take a search term
    - Perform a web search
Write a short 2–3 paragraph summary (under 300 words) that captures the key points without fluff.
The agent is built to always use a search tool when answering, but if GPT-5 is the model, 
it just lets GPT-5 decide automatically how to use the tool.
"""

from agents import Agent, WebSearchTool, ModelSettings

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

model = "gpt-5"
if model == "gpt-5":
    tools=["auto"]
else:
    tools=[WebSearchTool(search_context_size="low")]

search_agent = Agent(
    name = "Search agent",
    instructions = INSTRUCTIONS,
    tools = tools,
    model = model,
    model_settings = ModelSettings(tool_choice="required"),
)
