# -------------------------------------------------------------
# Imports: Core ADK classes (Agent, AgentTool) + local tools
# -------------------------------------------------------------
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

MODEL_NAME = "gemini-2.0-flash"

# Custom tools from your project "Smart Shopping Agent"
from google.adk import Agent
from Shopping_Bot.tools import generate_search_text_tool, google_search_grounding

# =============================================================
# 1) AGENT:search_text_agent
# -------------------------------------------------------------
# PURPOSE:
#   Takes a user's shopping-requirements JSON and converts it
#   into a clean, human-friendly Google search query.
#
# USED BY:
#   purchase_link_suggestor (as an internal tool)
# =============================================================
search_text_agent = Agent(
    name="SearchTextGeneratorAgent",
    model=MODEL_NAME,
    description="""
        An agent that converts a user's shopping-requirements JSON into
        a human-friendly search text suitable for Google search.
   """,
    tools=[generate_search_text_tool]
)


# =============================================================
# 2) AGENT: link_provider_agent
# -------------------------------------------------------------
# PURPOSE:
#   Takes the search text and fetches actual purchasable items
#   using google_search_grounding.
#
# BEHAVIOR:
#   - Calls the Google Search Grounding tool.
#   - Filters & formats results into clean product listings.
#   - Enforces rules: no redirect URLs, max 20 items, etc.
#
# USED BY:
#   purchase_link_suggestor (chained after search_text_agent)
# =============================================================
link_provider_agent = Agent(
    model=MODEL_NAME,
    name="link_provider_agent",
    description="Provides user with a list of clothing items fulfilling the criteria mentioned on the seach text",
    instruction="""
        You provide the FINAL response to the user: a list of purchasable clothing products
        that best match the search text.

        HOW TO WORK:
        - Always call the google_search_grounding agent tool with the user's query.
        - Use its response to construct a clean, user-facing list of products.
        - Your goal is to give the user USEFUL options, not to refuse or apologize.

        MATCHING & FALLBACK BEHAVIOR:
        - Prioritize products that match:
            • Item type (e.g., shirt), gender, size, fabric, and color
            • Price range (e.g., 1000–1500)
        - Treat phrases like “for birthday party” as hints about style or formality,
          NOT as strict filters that would cause you to return nothing.
        - If perfect matches are few:
            • Never say “I couldn't find exact matches” or “I couldn't find any items”.
            • Instead, return the best available options and clearly mention if:
                - The price is slightly outside the range
                - The size is close (e.g., M or XL instead of L)
                - The color is a very similar shade
        - Your answer must always contain some product options unless absolutely nothing is returned.

        LINKS:
        - Show ONLY real product links from shopping websites (Amazon, Flipkart, Myntra, Ajio, etc.).
        - Do NOT show:
            • Brand homepages
            • High-level category pages
            • Blogs or articles
            • Any internal redirect URL such as those starting with "https://vertexaisearch.cloud.google.com".
        - If the underlying tool response contains such redirect URLs, ignore them and only surface URLs
          that are clearly real product pages on known e-commerce domains.

        RESULT COUNT:
        - Limit your response to a MAXIMUM of 20 items.
        - Prefer 5–15 strong matches over 20 weak or generic links.

        RESPONSE FORMAT (MANDATORY):
        - Use bullet points.
        - For EACH item include:
            • Product Name  
            • Short, relevant description (e.g., "Red cotton shirt, size L, approx. ₹1299, suitable for a birthday party")  
            • Direct purchase link (product-specific URL on a shopping site, not a redirect URL)

        IMPORTANT:
        - Do NOT invent or fabricate URLs.
        - Do NOT respond with only explanations or apologies; always provide product options
          when the tool returns any remotely relevant products.
    """,
    tools=[google_search_grounding]    
)


# =============================================================
# 3) AGENT: purchase_link_suggestor  (Main Orchestration Agent)
# -------------------------------------------------------------
# WORKFLOW:
#   1. Takes a user's JSON requirements.
#   2. Passes the JSON → search_text_agent to create search text.
#   3. Sends that search text → link_provider_agent to fetch real shopping links.
#   4. Returns both:
#       - The generated search text
#       - The final product list
#
# NOTES:
#   - Uses AgentTool() to call other Agents as tools in sequence.
# =============================================================
purchase_link_suggestor = Agent(
    model = MODEL_NAME,
    name="purchase_link_suggestor",
    description="Provide a human-friendly search text suitable for Google search based on the JSON script provided",
    instruction="""
        You are an agent that is provided with a JSON script containing a user's shopping-requirements.
        Use the search_text_agent tool to create a human-friendly search text suitable for Google search.
        Provide the JSON script to the search_text_agent and then provide the response from the agent to the user.
        After that provide the search text to link_provider agent.
        """,

# Step 1 : AgentTool(agent=search_text_agent) Generate search text
# STep 2 : AgentTool(agent=link_provider_agent) Retrieve product links
    tools=[AgentTool(agent=search_text_agent), AgentTool(agent=link_provider_agent)]
)


