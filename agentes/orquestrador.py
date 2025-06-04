from agentes.agente_ingestao import AgenteIngestao
from agentes.agente_analise import AgenteAnalise
from agentes.agente_proposicao import AgenteProposicao
from agentes.agente_revisao import AgenteRevisao

class Orquestrador:
    def __init__(self):
        self.ingestao = AgenteIngestao()
        self.analise = AgenteAnalise()
        self.proposicao = AgenteProposicao()
        self.revisao = AgenteRevisao()

    def executar_fluxo(self, caminho_pecas: str, tipo_ato: str, modelo_ato: str, resumo: str):
        print("[1] Iniciando ingestão de peças...")
        processo = self.ingestao.executar(caminho_pecas)

        print("[2] Analisando peças e extraindo informações...")
        infos = self.analise.executar(processo)

        print("[3] Gerando ato com base no resumo...")
        ato = self.proposicao.executar(tipo_ato, modelo_ato, resumo)

        print("[4] Executando revisão final...")
        resultado_revisao = self.revisao.executar(ato, infos)

        return ato, infos, resultado_revisao
