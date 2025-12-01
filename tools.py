
import json
from google.adk.tools import FunctionTool
from google.adk.tools.google_search_tool import google_search
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

MODEL_NAME = "gemini-2.0-flash"

# Method to convert the JSON script into a natural,
# human-friendly Google-search style text.
def generate_search_text(shopping_json: dict) -> str:
    
    # Extracting and storing key-value mapping   
    category = shopping_json.get("Category", "")
    colour = shopping_json.get("Colour", "")
    gender = shopping_json.get("Gender", "")
    material = shopping_json.get("Material", "")
    occasion = shopping_json.get("Occasion", "")
    price_range = shopping_json.get("Price Range", "")
    size = shopping_json.get("Size", "")


    # Expand size abbreviation for clarity in output
    size_expanded = {
        "XS": "extra small",
        "S": "small",
        "M": "medium",
        "L": "large",
        "XL": "extra large",
        "XXL": "double extra large"
    }.get(size.upper(), size)


    # Generating the search sentence
    search_sentence = (
        f"Searching for {colour.lower()} {material.lower()} {category.lower()} "
        f"of size {size.upper()} ({size_expanded}) for {gender.lower()} "
        f"within price range {price_range} for {occasion.lower()}."
    )


    return search_sentence.strip()

# Adding the generate_search_text() method to function tool
generate_search_text_tool = FunctionTool(func=generate_search_text)

# Agent to search for products relevant to the User Requirements
_search_agent = Agent(
    model=MODEL_NAME,
    name="google_search_agent",
    description="An agent providing Google-search grounding capability",
    instruction= """
        Your job is to convert the user's search text into a list of REAL clothing products
        that can be directly purchased online.

        HOW TO USE google_search:
        - ALWAYS call the google_search grounding tool with a PRODUCT-FOCUSED query.
        - When building the query, include:
            • Item type and attributes (e.g., "red cotton shirt size L men")
            • Purchase intent keywords like "buy", "online", "price", "shopping"
            • The price band when provided (e.g., "1000-1500")
        - Treat context like "for birthday party" as a STYLE hint only (smart/casual/party),
          NOT as a strict filter that blocks results.

        FILTERING RESULTS:
        - From the search results, select links that clearly look like PRODUCT PAGES.
        - Prefer URLs from shopping sites (e.g. amazon.in, flipkart.com, myntra.com, ajio.com, tatacliq.com, zara.com, hm.com, etc.).
        - IGNORE:
            • Category landing pages (e.g. “Men’s fashion at ZARA”)
            • Brand homepages
            • Blogs, articles, or general info pages
            • Any URL that contains "vertexaisearch.cloud.google.com" or similar internal redirect domains

        APPROXIMATIONS:
        - Try to respect all constraints (color, size, fabric, gender, price range).
        - If you cannot find perfect matches:
            • Relax constraints slightly (e.g., price ±10–15%, similar shade of red, similar size like M/L if L is rare).
            • DO NOT ever say you “couldn’t find exact matches”.
            • Instead, clearly mention when an item is an approximate match (e.g., “slightly above the price range”).

        RESULT COUNT:
        - Aim to return 5–20 relevant products.
        - Do NOT stop after just 1 item if more relevant products are available.

        RESPONSE FORMAT (MANDATORY):
        - Always respond in bullet points.
        - For EACH product, include:
            • Product Name  
            • One-line useful description (mention at least: color, fabric, size, approximate price, and suitability if possible)  
            • Direct purchase link to the product page (must be a URL on a shopping site, NOT an internal redirect)

        IMPORTANT:
        - Do NOT invent or hallucinate URLs.
        - Only use URLs that come from the google_search tool output and look like valid product pages.
        - Never output internal redirect URLs such as those starting with "https://vertexaisearch.cloud.google.com".
    """,
    tools=[google_search]
)

google_search_grounding = AgentTool(agent=_search_agent)



