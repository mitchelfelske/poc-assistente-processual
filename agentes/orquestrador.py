from agentes.agente_memoria import AgenteMemoria
from agentes.agente_ingestao import AgenteIngestao
from agentes.agente_analise import AgenteAnalise
from agentes.agente_proposicao import AgenteProposicao
from agentes.agente_revisao import AgenteRevisao

class Orquestrador:
    def __init__(self):
        self.memoria = AgenteMemoria()
        self.ingestao = AgenteIngestao()
        self.analise = AgenteAnalise()
        self.proposicao = AgenteProposicao()
        self.revisao = AgenteRevisao()

    def executar_fluxo(self, caminho_pecas: str, tipo_ato: str, modelo_ato: str, resumo: str):
        print("[1] Iniciando ingestão de peças...")
        processo = self.ingestao.executar(caminho_pecas)
        
        print("[2]  Limpa histórico da memória antes de agregar...")
        self.memoria.limpar_historico()

        print("[3] Analisando peças e extraindo informações...")
        for peca in processo['peças']:
            infos_peca = self.analise.executar(peca)
            self.memoria.adicionar(infos_peca)

        print("[4] Obtendo informações históricas do processo...")
        self.memoria.agregar_informacoes_pecas()
        infos_processo = self.memoria.obter_historico()
        print(f"Informações do processo: {infos_processo}")

        print("[5] Gerando ato com base no resumo...")
        ato = self.proposicao.executar(tipo_ato, modelo_ato, resumo)

        print("[6] Executando revisão final...")
        resultado_revisao = self.revisao.executar(ato, infos_processo)

        return ato, infos_processo, resultado_revisao
