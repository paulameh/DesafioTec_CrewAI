import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

import os

from crewai import Agent, Task, Crew, LLM

from wikiAPI_tool import WikipediaSearchTool
wikipedia = WikipediaSearchTool()

llm_d = LLM(
     api_key = os.getenv("GEMINI_API_KEY"),
     model = "gemini/gemini-2.0-flash"
)

researcher = Agent(
    role="Pesquisador sênior",
    goal="Pesquisar informações verídicas e relevantes sobre {assunto}",
    backstory="Você é um pesquisador com muitos anos de experiência\n"
              "Você busca informações sobre {assunto}\n"
              "Você deve se comunicar somente através da língua portuguesa",
     allow_delegation=False,
     tools= [wikipedia],
     verbose=True
)

writer = Agent(
    role="Escritor sênior",
    goal="Escrever um artigo sobre o assunto: {assunto}",
    backstory="Você é um escritor com muitos anos de experiência\n"
              "Você utiliza as informaçoes coletadas pelo Pesquisador para escrever sobre {assunto}\n"
              "Seus textos são cativantes, e buscam informar e entreter o leitor, "
              "leve em consideração que o leitor pode não possuir conhecimentos aprofundados sobre {assunto}"
              "Você tem um conhecimento vasto sobre às normas da língua portuguesa "
              "e não costuma cometer erros ortográgicos, gramaticais ou de sinais\n"
              "O Seu texto não deve possuir tags de html\n "
              "Por fim, envie o seu texto para o Revisor sênior\n"
              "Você deve se comunicar somente através da língua portuguesa",
    allow_delegation=False,
    verbose=False
)

reviser = Agent(
    role="Revisor sênior",
    goal="Revisar o texto produzido pelo Escritor sobre {assunto}",
    backstory="Você é um revisor com muitos anos de experiência\n"
            "Você sempre oferece o texto sendo trabalhado ao requisitar ajuda de seus colegas\n"
            "Additional rules for Tools:\n"
            "-----------------"
            "1. Regarding the Action Input (the input to the action, just a simple python dictionary, enclosed"
            "in curly braces, using '\' to wrap keys and values.)\n"
            "For example for the following schema: \n"
            "class ExampleToolInput(BaseModel):\n"
                "task: str = Field(..., description='The task to delegate')\n"
                "context: str = Field(..., description='The context for the task')\n"
                "coworker: str = Field(..., description='The role/name of the coworker to delegate to')\n"
            "Then the input should be a JSON object with the user ID:\n"
            "- task: The task to delegate\n"
            "- context: The context for the task\n"
            "- coworker: The role/name of the coworker to delegate to\n"
            "Você deve se comunicar somente através da língua portuguesa",
    allow_delegation=True,
    verbose=False
)

research = Task(
    description=(
        "Busque informações verdadeiras, atuais e relevantes sobre: {assunto}\n"
        # "As fontes de sua pesquisa deverão ser mencionadas ao final, "
        # "sem haver a repetição de uma mesma fonte\n"
    ),
    expected_output="Um resumo com informações verdadeiras, atuais e relavantes sobre: {assunto} "
        "",
    agent=researcher,
)

write = Task(
    description=(
        "Use o material disponibilizado pelo Pesquisador sênior "
        "para escrever um texto com no mínimo 300 e no máximo {max} palavras, "
        "sobre o assunto: {assunto}.\n"
        "Não se esqueça de adicionar um título cativante e "
        "leve em consideração que seu texto será publicado como um artigo para um website\n"
        "Não cometa qualquer erro de sinalização, gramtical ou ortográfico"
    ),
    expected_output="Um texto sobre {assunto} com no mínimo 300 e no máximo {max} palavras e "
        "sem erros de sinais, gramaticais ou ortográficos"
        "seguindo o formato de artigo para website\n",
    agent=writer,
)

revise = Task(
    description=(
         "Veja se o texto produzido possui um título e se é capaz de entreter e informar o leitor\n"
         "Veja se o texto está dentro do modelo de artigo para website\n"
         "Veja se existe no mínimo 300 palvras e no máximo {max} no texto\n"
         "Verifique se há erros de sinais, gramaticais ou ortográficos no texto, "
         "se houver, corrija-os\n"
         ""
     ),
    expected_output="Um texto com no mínimo 300 e no máximo {max} palavras, "
                    "sem erros de sinais, gramaticais ou ortográgicos, "
                    "no modelo de artigo para website",
    agent=reviser
)

crew = Crew(
    agents=[researcher, writer, reviser],
    tasks=[research, write, revise],
    llm=llm_d,
    verbose=True,
    embedder={
            "provider": "google",
            "config": {
                 "model": "models/gemini-embedding-exp-03-07",
                 "api_key": os.getenv("GEMINI_API_KEY"),
                 "title": "Embeddings for Embedchain"
                 },
    },
    memory=True
)

result = crew.kickoff(inputs={"assunto": "Império Inca", "max": "500"})

print(result)
    