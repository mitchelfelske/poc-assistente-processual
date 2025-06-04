import os
import re
from dotenv import load_dotenv
from openai import AzureOpenAI

from agentes.interface_agente import AgenteInterface

class AgenteAnalise(AgenteInterface):
    def __init__(self):
        load_dotenv()
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )

    def extrair_informacoes(self, texto: str) -> dict:
        dados = {}

        if m := re.search(r"(R\\$|R\$)\s?([\d\.,]+)(?![\d\.,])", texto):
            dados["valor_mencionado"] = f"{m.group(1)} {m.group(2)}".rstrip('.,')

        if m := re.search(r"(?i)tribunal de contas|TCE", texto):
            dados["órgão_mencionado"] = "Tribunal de Contas"

        if m := re.search(r"(?i)(prazo de \d+ dias)", texto):
            dados["prazo_mencionado"] = m.group(1)

        return dados

    def resumir_peca(self, texto: str, max_tokens=300) -> str:
        prompt = f"""
            Você é um assistente jurídico. Resuma a seguinte peça processual em até 5 linhas, destacando o assunto principal, partes envolvidas e eventuais apontamentos relevantes:

            "{texto}"
        """
        response = self.client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def agregar_informacoes_pecas(self, infos, valores_agregados):
        for chave, valor in infos.items():
            valores = valor if isinstance(valor, list) else [valor]
            if chave not in valores_agregados:
                valores_agregados[chave] = []
            for v in valores:
                if v not in valores_agregados[chave]:
                    valores_agregados[chave].append(v)

    def executar(self, processo: dict) -> dict:
        # Processo é o dict com as peças e metadados
        informacoes_agregadas = {}
        for peca in processo["peças"]:
            infos = self.extrair_informacoes(peca["texto"])
            self.agregar_informacoes_pecas(infos, informacoes_agregadas)
        return informacoes_agregadas