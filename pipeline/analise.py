import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

def resumir_peca(texto: str, max_tokens=300) -> str:
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_KEY"),  
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )
    
    """Gera um resumo da peça processual com Azure OpenAI."""
    prompt = f"""
Você é um assistente jurídico. Resuma a seguinte peça processual em até 5 linhas, destacando o assunto principal, partes envolvidas e eventuais apontamentos relevantes:

"{texto}"
"""
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


def extrair_informacoes(texto: str) -> dict:
    """Extrai informações estruturadas da peça com base em padrões simples."""
    import re

    dados = {}

    if m := re.search(r"(R\\$|R\$)\s?([\d\.,]+)(?![\d\.,])", texto):
        dados["valor_mencionado"] = f"{m.group(1)} {m.group(2)}".rstrip('.,')


    if m := re.search(r"(?i)tribunal de contas|TCE", texto):
        dados["órgão_mencionado"] = "Tribunal de Contas"

    if m := re.search(r"(?i)(prazo de \d+ dias)", texto):
        dados["prazo_mencionado"] = m.group(1)

    return dados

def agregar_informacoes_pecas(infos, valores_agregados):
    for chave, valor in infos.items():
        # transforma valor em lista para uniformizar
        valores = valor if isinstance(valor, list) else [valor]

        if chave not in valores_agregados:
            valores_agregados[chave] = []

        for v in valores:
            if v not in valores_agregados[chave]:
                valores_agregados[chave].append(v)
