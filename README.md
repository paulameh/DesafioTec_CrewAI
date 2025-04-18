# Gerador de artigos com CrewAI e API da Wikipedia

Este projeto busca gerar artigos de qualquer assunto, com no mínimo 300 e no máximo 500 palavras (por padrão) com Inteligência artificial. 

Neste sistema, o usuário pode selecionar um assunto e, se preferir, um número máximo personalizado de palavras para o artigo a ser gerado, o qual será apresentado em uma página web utilizando notação pydantic, contendo os campos: title, key_words e content.

## Preparando o ambiente

Adicionar em uma arquivo .env :

    MODEL=gemini/gemini-2.0-flash
    GEMINI_API_KEY= [**Chave de API da google/gemini**]
    ACCESS_TOKEN= [**Chave de API da Wikimedia**]

E por fim, instale as bibliotecas em `requirements.txt`

## Executando o sistema

1. Executar o arquivo `sistemaAPI.py`
2. Abrir em seu navegador a url: localhost:8000/artigo/**Assunto**/**Max**
    * **Assunto**: é onde você deverá escrever o tema do artigo a ser escrito.
    * **Max** (Opcional, por padrão 500) : se refere a um número que representa o nº máximo palavras desejadas no artigo.
