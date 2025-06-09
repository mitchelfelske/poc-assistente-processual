import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class AgenteContexto:
    def __init__(self, agente_memoria):
        self.memoria = agente_memoria
        load_dotenv()
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
        self.deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    def gerar_linha_do_tempo(self, historico: list) -> list:
        """
        Gera uma linha do tempo cronológica a partir do histórico de peças.
        Cada item conterá: data, peça, parte(s) envolvida(s) e uma descrição curta.
        """
        eventos = []
        for item in sorted(historico, key=lambda x: x['timestamp']):
            dados = item['dados']
            partes = ', '.join(dados.get('NER', {}).get('partes', []))
            evento = {
                'data': item['timestamp'][:10],
                'peca': item['peca'],
                'partes': partes,
                'descricao': item['resumo']
            }
            eventos.append(evento)
        return eventos

    def gerar_resumo_narrativo(self, historico: list) -> str:
        """
        Gera um resumo narrativo da evolução do processo com base no histórico completo.
        """
        # Compilar informações dos resumos + dados
        narrativas = []
        for item in sorted(historico, key=lambda x: x['timestamp']):
            resumo = item['resumo']
            dados = item['dados']
            topicos = ', '.join(dados.get('topicos', []))
            partes = ', '.join(dados.get('NER', {}).get('partes', []))
            opinioes = [
                f"{op['target']} ({op['sentimento']})"
                for op in dados.get('opinioes', [])
            ]
            opinioes_str = '; '.join(opinioes)
            narrativa = f"- {resumo} | Partes: {partes} | Tópicos: {topicos} | Opiniões: {opinioes_str}"
            narrativas.append(narrativa)

        texto_base = "\n".join(narrativas)

        system_prompt = """
            Você é um analista jurídico responsável por gerar uma narrativa formal e concisa do histórico de um processo de contas públicas.
            Seu objetivo é produzir um resumo coeso, em terceira pessoa, descrevendo a evolução do processo com base nas peças analisadas.

            Utilize os dados fornecidos abaixo para redigir um resumo que:
            - Descreva o que aconteceu no processo até o momento.
            - Destaque as partes envolvidas e os principais tópicos discutidos.
            - Mencione os sentimentos associados a cada tema (ex: positivo, negativo, neutro).

            Seja claro, direto e utilize linguagem institucional apropriada para um tribunal de contas.
        """

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto_base}
            ],
            temperature=0.3,
            max_tokens=600
        )

        return response.choices[0].message.content.strip()
