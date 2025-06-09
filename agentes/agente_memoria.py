
from datetime import datetime

class AgenteMemoria():
    """ 
        Agente responsável por armazenar informações extraídas de peças processuais. 
        Mantém um histórico de informações/eventos do processo.
        Pode ser consultada posteriormente para fornecer informações contextuais do processo.
    """
    def __init__(self):
        self.historico = []

    def obter_historico(self):
        return self.historico
    
    def limpar_historico(self):
        """
            Limpa o histórico de informações armazenadas.
        """
        self.historico = []

    def adicionar(self, peca_id: str, dados: dict, resumo: str):
        """
            Adiciona informações extraídas de cada peça ao histórico.
            Recebe um dicionário com as informações a serem armazenadas.
        """
        evento = {
            'peca': peca_id,
            'resumo': resumo,
            'dados': dados,
            'timestamp': datetime.now().isoformat()
        }
        self.historico.append(evento)
