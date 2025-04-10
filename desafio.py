import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, LLM

llm_d = LLM(model="gemini/gemini-2.0-flash")

researcher = Agent(
    role="Pesquisador",
    goal="Pesquisar sobre {assunto} para a criação de um artigo para um website",
    backstory="Você é um pesquisador eficiente\n"
              "Você busca informações relevantes sobre {assunto}"
              "de modo a possibilitar a escrita de um artigo em um website\n"
              "",
     allow_delegation=False,
     verbose=True
)

writer = Agent(
    role="Escritor",
    goal="Escrever um artigo sobre o assunto: {assunto}",
    backstory="Você é um excelente escritor\n"
              "Você utiliza as informaçoes coletadas pelo Pesquisador para escrever sobre {assunto} \n"
              "Seus textos também buscam informar e entreter o leitor",
    allow_delegation=False,
    verbose=True
)

reviser = Agent(
    role="Revisor",
    goal="Revisar o texto produzido pelo Escritor sobre {assunto}"
         "corrigindo erros de sinais, gramaticais ou ortográficos se houverem",
    backstory="Você é um revisor dedicado e muito competente\n"
              "Suas revisões são precisas",
    allow_delegation=False,
    verbose=True
)

research = Task(
    description=(
        "Busque informações atuais e relevantes para o tema: {assunto}\n"
        "Os resultados de sua pesquisa devem ser organizados dentro das categorias: \n"
              "1. Introdução\n"
              "2. Conteúdo\n"
              "3. Conclusão\n"
              "4. Palavras chave\n"
              "As fontes de sua pesquisa deverão ser mencionadas ao final, "
              "sem haver a repetição de uma mesma fonte, e organizadas em ordem alfabética\n"
              "Esse material servirá de base para o Escritor"
    ),
    expected_output="Um resumo com informações relevantes sobre {assunto} "
        "organizado em introdução, conteúdo, conclusão, Palavras chave e referências",
    agent=researcher,
)

write = Task(
    description=(
        "Use o material disponibilizado pelo pesquisador"
        "para escrever um texto com no mínimo 300 palavras no modelo de artigo para website"
        " sobre o assunto: {assunto}.\n"
        "Utilize as informações presentes em 1. Introdução, 2. Conteúdo e 3. Conclusão"
		"E organize seu texto considerando essas classificações\n"
        "Utilize as palavras-chave disponibilizadas\n"
        "Ao final, cite as referências utilizadas e as apresente em ordem alfabética"
    ),
    expected_output="Um texto sobre {assunto} com no mínimo 300 palavras e sem erros de sinais, gramaticais ou ortográficos"
        "em formato de artigo de website\n"
        "possuindo ao fim as referências organizadas em ordem alfabética",
    agent=writer,
)

revise = Task(
    description=(
         "Verifique a veracidade das informações no texto produzido pelo Escritor "
         "e caso encontre informações incorretas as substitua pelas corretas\n"
         "Confirme a existência de uma estrutura textual, contendo introdução, desenvolvimento e conclusão "
         "no modelo de artigo para website e corrija o texto se não encontrar essa estrutura\n"
         "Veja se existe no mínimo 300 palvras no texto, e caso não haja complemente-o de forma a alcançar esta meta\n"
         "Se houver, corrija erros de sinais, gramaticas ou ortográgicos\n"
         "Não permita que uma mesma referência seja mencionada mais de uma vez no texto"
     ),
    expected_output="Um texto com no mínimo 300 palavras, "
                    "sem erros de sinais, gramaticais ou ortográgicos no modelo de artigo para website",
    agent=reviser
)

crew = Crew(
    agents=[researcher, writer, reviser],
    tasks=[research, write, revise],
    verbose=True,
    llm=llm_d
)



result = crew.kickoff(inputs={"assunto": "Taekwondo"})

print(result)
