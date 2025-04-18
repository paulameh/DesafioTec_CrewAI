# Recursos para carregar as variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()
import os

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Criando o custom tool
from crewai.tools import BaseTool

class WikipediaSearchTool(BaseTool):
    name: str ="Ferramenta de pesquisa na Wikipédia"
    description: str = ("Utiliza a API da Wikipédia para encontrar informações")
    
    def _run(self, argument: str) -> str:
      """
        Procurar informações na Wikipédia
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
        "exlimit": "1",
      }

      # Fazendo a requisição
      import requests

      response = requests.get("https://pt.wikipedia.org/w/api.php", headers=headers, params=parameters)
      data = response.json()

      # Testando se há resultados para a pesquisa
      # no caso de não haver a mensagem aparecerá no terminal
      # para ver isso, mude verbose da crew para true e descomente o print em crewArtigo.py
      try:
        return data['query']['pages'][0]['extract']
      except:
        return f"Sem resultados para a pesquisa de {argument} na Wikipédia, tente repetir a pesquisa de outra forma"
