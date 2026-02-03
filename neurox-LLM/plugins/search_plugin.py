from core.plugin_interface import NeuroxPlugin
import requests
from bs4 import BeautifulSoup
import urllib.parse
import ollama

class SearchPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Search Plugin"
        self.description = "Performs web searches."
        self.order = 20

    def execute(self, context: dict) -> dict:
        if 'search_query' in context and not context.get('search_results'):
            query = context['search_query']
            
            # Optimization
            if len(query.split()) > 6:
                try:
                    refine_prompt = f"Extract a concise Google search query from: '{query}'. Return ONLY the query."
                    model = context.get('model_name', 'phi3')
                    resp = ollama.chat(model=model, messages=[{'role': 'system', 'content': refine_prompt}], stream=False)
                    query = resp['message']['content'].strip().strip('"')
                except:
                    pass
            
            print(f"[{self.name}] Searching: {query}")
            results = self._search_web(query)
            return {'search_results': results}
        return None

    def _search_web(self, query, max_results=5):
        try:
            url = "https://html.duckduckgo.com/html/"
            payload = {'q': query}
            headers = {"User-Agent": "Mozilla/5.0 ..."}
            
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code != 200: return "Error retrieving results."

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            for result in soup.find_all('div', class_='result'):
                title_tag = result.find('a', class_='result__a')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag['href']
                    results.append(f"Title: {title}\nLink: {link}\n")
                if len(results) >= max_results: break
                    
            return "\n".join(results) if results else "No results found."
        except Exception as e:
            return f"Error: {e}"
