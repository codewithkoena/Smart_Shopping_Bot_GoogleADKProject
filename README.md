\# 🛍️ Smart Shopping Agent  

\### An AI-powered multi-agent system that turns natural language clothing requests into real purchasable product links.



---



\## 🚀 Overview



The \*\*Smart Shopping Agent\*\* is a multi-agent AI system built using \*\*Google ADK (Agent Development Kit)\*\* and \*\*Gemini 2.0 Flash\*\*.  

It understands natural-language descriptions of clothing, extracts structured attributes (color, fabric, size, price, gender, category, occasion), generates optimized search queries, and fetches real purchasable product links from popular ecommerce platforms using \*\*Google Search Grounding\*\*.



This project demonstrates:

\- multi-agent orchestration  

\- stateful natural-language understanding  

\- tool-calling pipelines  

\- grounded product search (no hallucinated URLs)  

\- clean, deterministic attribute extraction  



---



\## 🧠 Key Features



\### ✔ Natural Language Understanding  

Understands complex shopping requests like:  

> “I need a red cotton saree for a wedding under 1500 for my wife, size free.”



And turns them into a structured JSON.



\### ✔ Deterministic Shopping Requirement Extraction  

Extracts:

\- Gender  

\- Size  

\- Category  

\- Color  

\- Material  

\- Occasion  

\- Price Range  



\### ✔ Multi-Agent Architecture  

\- \*\*Root Agent\*\* – conversation manager  

\- \*\*update\_shopping\_state tool\*\* – extracts attributes  

\- \*\*search\_text\_agent\*\* – converts JSON → optimized search text  

\- \*\*link\_provider\_agent\*\* – fetches real product links  

\- \*\*purchase\_link\_suggestor\*\* – orchestrates the last two agents  



\### ✔ Real Product Links via Google Search Grounding  

Outputs 5–20 valid links from sites like:

\- Amazon  

\- Flipkart  

\- Myntra  

\- Ajio  

\- TataCliq  



No fabricated URLs. No redirect URLs.



\### ✔ Smart Fallback Behavior  

If perfect matches are rare:

\- relaxes price slightly  

\- suggests close color or size matches  

\- never says “I couldn’t find anything”  



---



\## 🏗️ Architecture Diagram

                         ┌─────────────────────────┐
                         │     User Message        │
                         └────────────┬────────────┘
                                      │
                                      ▼
                     ┌────────────────────────────────────┐
                     │          ROOT AGENT                │
                     │  (smart_shopping_agent)            │
                     │  - Greets user                     │
                     │  - Maintains conversation state    │
                     │  - Detects missing fields          │
                     └───────────────┬────────────────────┘
                                     │ calls tool
                                     ▼
                 ┌──────────────────────────────────────────┐
                 │      update_shopping_state() Tool        │
                 │  - Regex & rule-based extractors         │
                 │  - Builds JSON requirements              │
                 │  - Returns state + missing fields        │
                 └───────────────┬──────────────────────────┘
                                 │
                     Missing     │ Yes → Ask follow-up
                     fields?     │
                              ┌──▼──┐
                              │User │
                              └─────┘
                                 │ No
                                 ▼
                 ┌────────────────────────────────────────────┐
                 │      purchase_link_suggestor Agent        │
                 │  - Takes completed JSON                    │
                 │  - Calls search_text_agent                 │
                 │  - Calls link_provider_agent               │
                 └───────────────┬────────────────────────────┘
                                 │
               ┌─────────────────┴──────────────────┐
               ▼                                    ▼
  ┌──────────────────────────┐          ┌──────────────────────────┐
  │   search_text_agent      │          │   link_provider_agent    │
  │ - JSON → human-friendly  │          │ - Calls google grounding │
  │   search query           │          │ - Filters product pages  │
  │                          │          │ - Returns 5–20 items     │
  └──────────────┬───────────┘          └───────────────┬──────────┘
                 │                                         │
                 └──────► Final Response to User ◄─────────┘
                   (search text + curated purchasable links)





