import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from agentes.interface_agente import AgenteInterface

class AgenteAnalise(AgenteInterface):
    def __init__(self):
        load_dotenv()
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
        self.deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    def extrair_informacoes_estruturadas(self, texto: str) -> dict:
        system_prompt = f"""
            Você é um assistente jurídico especializado em extrair informações estruturadas de peças processuais.
            Cada processo se refere a um caso específico e está relacionado ao contexto de um Tribunal de Contas.
            Um Tribunal de Contas é um órgão responsável por fiscalizar a aplicação de recursos públicos e garantir a legalidade, legitimidade e economicidade dos atos administrativos.
            O processo pode conter informações sobre prestações de contas, relatórios de controle interno, pareceres técnicos, notificações e defesas.
            Cada processo pode conter informações como partes, valores, prazos, datas, tópicos, opiniões e PII (informação pessoal identificável).
            Analise o texto a seguir e extraia Named Entity Recognition (NER), Personally Identifiable Information (PII), análise de tópicos e opiniões de sentimento.
            Retorne um JSON com as seguintes informações:
            - NER (Named Entity Recognition):
                - órgão_mencionado (string, ex: "Tribunal de Contas")
                - partes (lista de strings)
                - valores (lista de strings, ex: "R$ 920.000,00")
                - prazos (lista de strings, ex: "15 dias úteis")
                - datas (lista de strings)
            - PII (Personally Identifiable Information):
                - nomes (lista de strings)
                - emails (lista de strings)
                - telefones (lista de strings)
                - CPF/CNPJ (lista de strings)
            - topicos (lista de strings)
            - opinioes (lista de objetos com target e sentimento)

            Responda apenas no formato dicionário (par "chave": "valor") passível de extrair o json.
        """

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto}
            ],
            temperature=0,
            max_tokens=500
        )

        print(f"Resposta do modelo para informações estruturadas:\n {response.choices[0].message.content.strip()}")

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Em caso de falha, retorna vazio
            return {}

    def resumir_peca(self, texto: str, infos: str, max_tokens=300) -> str:

        system_prompt = f"""
            Você é um assistente jurídico especializado em extrair informações estruturadas de peças processuais.
            Cada processo se refere a um caso específico e está relacionado ao contexto de um Tribunal de Contas.
            Um Tribunal de Contas é um órgão responsável por fiscalizar a aplicação de recursos públicos e garantir a legalidade, legitimidade e economicidade dos atos administrativos.
            O processo pode conter informações sobre prestações de contas, relatórios de controle interno, pareceres técnicos, notificações e defesas.
            Faça um resumo utilizando linguagem formal, o mais direto e conciso possível.
            Utilize a terceira pessoa do singular e evite o uso de advérbios.
            O resumo deve conter as principais informações extraídas do texto, que estão disponibilizadas a seguir.

            "{infos}"
        """

        response = self.client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto}
            ],
            temperature=0.2,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def executar(self, peca: dict) -> dict:
        infos = self.extrair_informacoes_estruturadas(peca['texto'])
        resumo = self.resumir_peca(peca['texto'], infos)
        return infos, resumo
