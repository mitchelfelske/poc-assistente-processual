from agentes.agente_memoria import AgenteMemoria
from agentes.agente_contexto import AgenteContexto

from agentes.agente_ingestao import AgenteIngestao
from agentes.agente_analise import AgenteAnalise
from agentes.agente_proposicao import AgenteProposicao
from agentes.agente_revisao import AgenteRevisao

class Orquestrador:
    def __init__(self):
        self.memoria = AgenteMemoria()
        self.contexto = AgenteContexto(self.memoria)

        self.ingestao = AgenteIngestao()
        self.analise = AgenteAnalise()
        self.proposicao = AgenteProposicao()
        self.revisao = AgenteRevisao()

    def executar_fluxo(self, caminho_pecas: str, tipo_ato: str, modelo_ato: str):
        print("[1] Iniciando ingestão de peças...")
        processo = self.ingestao.executar_local(caminho_pecas)
        
        print("[2]  Limpa histórico da memória...")
        self.memoria.limpar_historico()

        print("[3] Analisando peças e extraindo informações...")
        for peca in processo['peças']:
            print(f"Analisando peça: {peca['arquivo']}")
            print(f"Texto: {peca['texto']}...") 
            dados_estruturados, resumo = self.analise.executar(peca)
            peca_id = peca['arquivo']
            self.memoria.adicionar(peca_id, dados_estruturados, resumo)

        print("[4] Obtendo informações históricas do processo...")
        historico = self.memoria.obter_historico()
        
        print(f"Informações do processo: {historico}")

        print("[5] Gerando linha do tempo e resumo narrativo...")
        linha_tempo = self.contexto.gerar_linha_do_tempo(historico)
        
        resumo_narrativo = self.contexto.gerar_resumo_narrativo(historico)
        
        print("[6] Gerando ato com base no resumo...")
        ato = self.proposicao.executar(tipo_ato, modelo_ato, resumo_narrativo)

        #print("[7] Executando revisão final...")
        #resultado_revisao = self.revisao.executar(ato, infos_processo)

        return linha_tempo, resumo_narrativo, ato
