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





