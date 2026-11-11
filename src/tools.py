# src/tools.py
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Busca Web DuckDuckGo")
def web_search_tool(query: str) -> str:
    """Realiza uma busca na web usando o DuckDuckGo e retorna os principais resultados contendo títulos, links e resumos."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(f"Título: {r.get('title')}\nLink: {r.get('href')}\nResumo: {r.get('body')}\n")
    return "\n---\n".join(results) if results else "Nenhum resultado encontrado."