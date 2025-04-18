# Crew a trabalhar
# Importando a crew que constrói o artigo
from crewArtigo import crewAI_artigo

# flask para a criação da API
from flask import Flask
app = Flask(__name__)

# Lidando com eventuais erros
@app.errorhandler(Exception)
def errorHandler4(e):
    return "<h2>Ops, há algum erro na URL pesquisada</h2> <hr>"  \
    "<strong>Abra em seu navegador a url:</strong> localhost:8000/artigo/<strong>Assunto</strong>/<strong>Max</strong> <br><br>" \
    "<strong>Assunto:</strong> é onde você deverá escrever o tema do artigo a ser escrito. <br>" \
    "<strong>Max</strong> (Opcional, por padrão 500) : número que representa o nº máximo palavras desejadas no artigo.</p>"


# Caso de não especificação do número máximo de palavras
@app.route('/artigo/<assunto>/')
def getArtigoByAssunto(assunto):

    if (str.isdecimal(assunto)):
        return f"<h2>Por favor, insira um assunto válido, e não {assunto}</h2>"
    
    result = crewAI_artigo(assunto, 500)
    return f"<p>{result}</p>"

# Caso de especificação do número máximo de palavras
@app.route('/artigo/<assunto>/<max>')
def getArtigo(assunto, max):
    
    if (not(str.isdecimal(max))):
        return f"<h2>O número de palavras deverá ser um número inteiro, e não: '{max}'</h2>"
    if (int(max) < 480):
        return "<h2>Por favor, insira um número máximo de palavras de no mínimo 480</h2>"
    
    if (str.isdecimal(assunto)):
        return f"<h2>Por favor, insira um assunto válido, e não {assunto}</h2>"
    
    result = crewAI_artigo(assunto, max)
    return f"<h2>Resultado da Crew</h2> <hr> {result}"

# Porto do servidor
app.run(port=8000)