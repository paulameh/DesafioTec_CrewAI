from dotenv import load_dotenv
load_dotenv()

import os
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
APP_NAME = os.getenv("APP_NAME")
EMAIL = os.getenv("EMAIL")

headers = {
  'Authorization': '{ACCESS_TOKEN}',
  'User-Agent': '{APP_NAME} ({EMAIL})'
}

title = 'Mitologia'

parameters = {
	"action": "query",
  "titles": f"{title}",
	"format": "json",
	"prop": "extracts",
  "explaintext": "2",
	"formatversion": "2",
  "exlimit": "20",
}

import requests

response = requests.get("https://pt.wikipedia.org/w/api.php", headers=headers, params=parameters)

data = response.json()
# print((data['query']['pages']))

for page in data['query']['pages']:
     print(page['extract'])

from crewai.tools import BaseTool

class WikipediaSearchTool(BaseTool):
    name: str ="Wikipedia Search Tool"
    description: str = ("Uses the Wikipedia API to research information")
    
    def _run(self, argument: str) -> str:
        # Your tool's logic here
        return "Tool's result"
     
