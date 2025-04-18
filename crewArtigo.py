def crewAI_artigo(assunto, max):
    import warnings
    warnings.filterwarnings('ignore')

    # Recursos para carregar as variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv()
    import os

    # Trazendo o CrewAI para o projeto
    from crewai import Agent, Task, Crew, LLM

    llm_d = LLM(
        api_key = os.getenv("GEMINI_API_KEY"),
        model = "gemini/gemini-2.0-flash"
    )

    # Definindo a notação pydantic a ser usada para o output da crew
    from pydantic import BaseModel, Field
    class Artigo(BaseModel):
        title: str = Field(description="Título do artigo")
        key_words: list = Field(description="Palavras-chave do conteúdo do artigo")
        content: str = Field(description="Conteúdo do artigo")

    # Custom tool
    from wikiAPI_tool import WikipediaSearchTool
    wikipedia = WikipediaSearchTool()


    researcher = Agent(
        role = "Pesquisador sênior",
        goal = "Pesquisar informações verídicas e relevantes sobre o(a) {assunto}",
        backstory = "Você é um pesquisador com muitos anos de experiência\n"
            "Você busca informações sobre {assunto}\n"
            "Você deve se comunicar somente através da língua portuguesa",
        allow_delegation=False,
        tools= [wikipedia],
        verbose=False
    )

    writer = Agent(
        role="Escritor sênior",
        goal="Escrever um artigo sobre o(a) {assunto}",
        backstory="Você é um escritor com muitos anos de experiência\n"
            "Você utiliza as informaçoes coletadas pelo Pesquisador sênior para escrever sobre o(a) {assunto}\n"
            "Seus textos buscam entreter e informar o leitor, "
            "utilizando um linguajar simples, e portanto acessível, evitando expressões complexas\n"
            "Você tem um conhecimento vasto sobre às normas da língua portuguesa "
            "e não costuma cometer erros ortográgicos, gramaticais ou de sinais\n"
            "O Seu texto não deve possuir tags de html\n"
            "Você deve se comunicar somente através da língua portuguesa",
        allow_delegation=False,
        verbose=False
    )

    # Em "Adiditional rules for tools" foi implementado uma solução para o correto funcionamento
    # da delegação de trabalhos entre os agentes

    reviser = Agent(
        role="Revisor sênior",
        goal="Revisar o texto produzido pelo Escritor sobre o(a) {assunto}",
        backstory="Você é um revisor com muitos anos de experiência\n"
            "Você sempre oferece o texto sendo trabalhado ao requisitar ajuda de seus colegas\n\n"
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
            "-----------------\n"
            "Você deve se comunicar somente através da língua portuguesa",   
        allow_delegation=True,
        verbose=False
    )

    research = Task(
        description=(
            "Busque informações verdadeiras, atuais e relevantes o(a) {assunto}\n"
            "Caso descubra dados ou conceitos complexos, "
            "busque suas definições"
        ),
        expected_output="Um resumo com informações verdadeiras, atuais e relavantes o(a) {assunto} ",
        agent=researcher,
    )

    write = Task(
        description=(
            "Use o material disponibilizado pelo Pesquisador sênior "
            "para escrever um texto com no mínimo 300 e no máximo {max} palavras, "
            "sobre o(a) {assunto}.\n"
            "Não se esqueça de adicionar um título cativante e "
            "leve em consideração que seu texto deverá ser simples, divertido e informativo, "
            "evitando palavras ou conceitos muito complexos\n"
            "Não cometa qualquer erro de sinalização, gramatical ou ortográfico"
        ),
        expected_output="Um texto sobre o(a) {assunto} com no mínimo 300 e no máximo {max} palavras e "
            "sem erros de sinais, gramaticais ou ortográficos.\n"
            "O texto também deve ser divertido, simples e informativo, sem muitos conceitos complexos",
        agent=writer,
    )

    revise = Task(
        description=(
            "Veja se o texto produzido poderia ser publicado como um artigo para website\n"
            "Veja se existe no mínimo 300 palvras e no máximo {max} no texto\n"
            "Caso o número máximo de palavras seja ultrapassado, reduza o número de palavras do texto\n"
            "Verifique se há erros de sinais, gramaticais ou ortográficos no texto, "
            "se houver, corrija-os"
        ),
        expected_output = "Um texto com no mínimo 300 e no máximo {max} palavras, "
            "sem erros de sinais, gramaticais ou ortográgicos, "
            "que possa ser publicado como um artigo para website",
        output_pydantic = Artigo,
        agent=reviser
    )

    # Na utilização do embedder haverá erros 429 de exaustão de recurso por uma limitação de rate do serviço
    # esse erro não pertuba na funcionalidade da crew, pelo contrário, possibilita o acesso a ferramentas
    # que impulsionam o funcionamento da LLM

    crew = Crew(
        agents=[researcher, writer, reviser],
        tasks=[research, write, revise],
        llm=llm_d,
        verbose=False,
        embedder={
                "provider": "google",
                "config": {
                    "model": "models/gemini-embedding-exp-03-07",
                    "api_key": os.getenv("GEMINI_API_KEY"),
                    },
        },
        memory=True
    )

    result = crew.kickoff(inputs={"assunto": assunto, "max": max})
    # print(result)
    return result



