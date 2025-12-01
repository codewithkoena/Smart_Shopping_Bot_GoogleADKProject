
import re
import json
from typing import Dict, Any
from google.adk.agents import Agent
from Shopping_Bot.supporting_agents import purchase_link_suggestor

# --------------------------------------------------------------------------
# Generating the JSON script based on all the requirements provided by 
# the user in the following format 
#   {
#             "Gender": '',
#             "Size":'',
#             "Occasion": '',
#             "Category": '',
#             "Colour": '',
#             "Material": '',
#             "Price Range": '',
# }
# --------------------------------------------------------------------------
def update_shopping_state(args: dict) -> dict:
    """
    ADK-compatible tool.
    Expects args = {"raw_query": "...", "current_state": {...}}
    Returns: {"state": {...}, "missing_fields": [...]}
    """
    raw_query = args.get("raw_query", "")
    text = raw_query.lower().strip()
    current_state = args.get("current_state")

    # Initialize state if empty
    if not current_state:
        current_state = {
            "Gender": None,
            "Size": None,
            "Occasion": None,
            "Category": None,
            "Colour": None,
            "Material": None,
            "Price Range": None,
        }

    # Extracting colour from the User text 
    if current_state["Colour"] is None:
        colours = [
            "red","blue","green","yellow","pink","black","white","purple","orange","magenta","indigo",
            "brown","maroon","gold","silver","beige","grey","gray"
        ]
        for c in colours:
            if re.search(rf"\b{c}\b", text):
                current_state["Colour"] = c.capitalize()
                break




    #Extracting category of the product from the User query
    if current_state["Category"] is None:
        category_map = {
            "saree": "Sarees",
            "kurti": "Kurtis",
            "kurta": "Kurtas",
            "shirt": "Shirts",
            "tshirt": "T-Shirts",
            "t-shirt": "T-Shirts",
            "lehenga": "Lehengas",
            "sherwani": "Sherwanis",
            "shoes": "Shoes",
            "mojri": "Mojris",
            "heels": "Heels",
            "shirts": "Shirts",
            "Shirts": "Shirts",
            "gown": "Gown",
            "purse": "Purse",
            "jeans": "Jeans",
            "jumpsuit": "Jumpsuit",
            "gown": "Gown",
            "dress": "Dress",
            "handbags": "Handbags",
            "Backpack": "Backpacks"
        }
        for k, v in category_map.items():
            if k in text:
                current_state["Category"] = v
                break




    # Extracting occasion to wear the product from the User query
    if current_state["Occasion"] is None:
        occasion_map = {
            "wedding": "Wedding",
            "reception": "Wedding Reception",
            "haldi": "Haldi",
            "mehendi": "Mehendi",
            "diwali": "Festive Wear Traditional",
            "christmas": "Christmas",
            "halloween": "Halloween",
            "office": "Formal Wear",
            "birthday": "Party Wear",
            "date night": "Date night",
            "meeting": "Formal Wear"
        }
        for phrase, lbl in occasion_map.items():
            if phrase in text:
                current_state["Occasion"] = lbl
                break




    # Extracting material of the product from the User query
    if current_state["Material"] is None:
        materials = ["cotton", "silk", "linen", "rayon", "velvet", "chiffon", "georgette"]
        for m in materials:
            if m in text:
                current_state["Material"] = m.capitalize()
                break

    # Extracting gender from the User query
    if current_state["Gender"] is None:

        # Direct Relationships
        if any(w in text for w in [" men", " men's", " man", "male", "boy", "boys", "husband", "groom", "father", "dad", "brother", "son", "boyfriend"]):
            current_state["Gender"] = "Men"
        elif any(w in text for w in ["women", "woman", "female", "bride", "bridal","girl", "girls", "ladies", "wife", "mother", "mom", "sister", "daughter", "girlfriend"]):
            current_state["Gender"] = "Women"

        # other sort of references for women
        women_refs = ["saree", "gown" , "jumpsuit" , "dress"]

        
        if any(word in text for word in women_refs):
            current_state["Gender"] = "Women"


    # Extracting size from the User query
       
    if current_state["Size"] is None:
        # Direct size words (Large, Medium, Small)
        size_words = {
            "small": "S",
            "medium": "M",
            "large": "L",
            "extra large": "XL",
            "extra-large": "XL",
            "extra small": "XS",
            "extra-small": "XS",
            
        }


        for phrase, code in size_words.items():
            if phrase in text:
                current_state["Size"] = code
                break

        # One-word sizes: L, M, S, XL, XXL, XS
        if current_state["Size"] is None:
            match = re.search(r"\b(XXL|XL|L|M|S|XS)\b", text.upper())
            if match:
                current_state["Size"] = match.group(1)


        # Numeric size (like size 40, 42)
        if current_state["Size"] is None:
            num = re.search(r"\bsize\s*(\d{2})\b", text)
            if num:
                current_state["Size"] = num.group(1)


    # Extracting price range from the User query
    if current_state["Price Range"] is None:
        under = re.search(r"(under|below|upto|up to)\s*₹?\s*(\d+)", text)
        if under:
            current_state["Price Range"] = f"0 - {under.group(2)}"
        else:
            between = re.search(r"between\s*₹?(\d+)\D+₹?(\d+)", text)
            if between:
                a, b = sorted([int(between.group(1)), int(between.group(2))])
                current_state["Price Range"] = f"{a} - {b}"
            else:
                dash = re.search(r"₹?(\d+)\s*-\s*₹?(\d+)", text)
                if dash:
                    a, b = sorted([int(dash.group(1)), int(dash.group(2))])
                    current_state["Price Range"] = f"{a} - {b}"




    # Check for the required fields that could not be obtained from the User query
    missing_fields = [k for k, v in current_state.items() if v is None]

    return {
        "state": current_state,
        "missing_fields": missing_fields,
    }


# --------------------------------------------------------------------------
#                             ROOT AGENT
# --------------------------------------------------------------------------
# Root Agent interacts with the user to collect all the requirements.
# It creates a JSON script consisting of all these requirements using 
# the update_shopping_state(). Once the complete JSON script is obtained,
# the correctly formatted JSON script is passed to purchase_link_generator agent

root_agent = Agent(
    name="smart_shopping_agent",
    model="gemini-2.0-flash",
    description="A smart shopping assistant that collects clothing preferences.",
    instruction=(
        "You are a step-by-step smart shopping assistant.\n\n"

        "FIRST TURN RULE:\n"
        "- If there is no conversation state OR this is the first user message,\n"
        "  IGNORE the user text and reply exactly:\n"
        "  \"Welcome! I am your smart shopping assistant. What are you looking for?\"\n"
        "- DO NOT call any tool on the first turn.\n\n"

        "AFTER FIRST TURN:\n"
        "1. Every time the user describes a product (e.g., \"red saree under 1000\"),\n"
        "   call update_shopping_state with:\n"
        "     raw_query = user's message\n"
        "     current_state = previous state (or null)\n\n"

        "2. The tool returns 'state' and 'missing_fields'.\n"
        "   If missing_fields is NOT empty, ask the user ONLY for those fields.\n\n"

        "3. When missing_fields *is empty*, pass the correctly formatted JSON script to purchase_link_generator agent\n"
    ),
    tools=[update_shopping_state],
   
   # Adding a sub-agent to provide product recommendation 
    sub_agents=[purchase_link_suggestor]
)














