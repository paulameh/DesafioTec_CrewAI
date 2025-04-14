from dotenv import load_dotenv
load_dotenv()

import os
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

from crewai.tools import BaseTool

class WikipediaSearchTool(BaseTool):
    name: str ="Ferramenta de pesquisa na Wikipédia"
    description: str = ("Usa a API da Wikipédia para encontrar informações")
    
    def _run(self, argument: str) -> str:
      """
        Procurar na Wikipédia informações
      """

      headers = {
        'Authorization': '{ACCESS_TOKEN}',
      }

      parameters = {
        "action": "query",
        "titles": argument,
        "format": "json",
        "prop": "extracts",
        "explaintext": "2",
        "formatversion": "2",
        "exlimit": "20",
      }

      import requests

      response = requests.get("https://pt.wikipedia.org/w/api.php", headers=headers, params=parameters)
      data = response.json()

      try:
        return data['query']['pages'][0]['extract']
      except:
        return f"Sem resultados para a pesquisa de {argument} na Wikipédia, tente repetir a pesquisa de outra forma"
