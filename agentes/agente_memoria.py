
from collections import defaultdict
from typing import Any, Dict, List

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

    def adicionar(self, info_extraida: dict):
        """
            Adiciona informações extraídas ao histórico.
            Recebe um dicionário com as informações a serem armazenadas.
        """
        self.historico.append(info_extraida)
    
    def agregar_informacoes_pecas(self) -> None:
        """
        Agrega todas as informações extraídas das peças,
        unificando os valores por chave, removendo duplicatas e preservando a ordem.

        Atualiza `self.historico` para conter um dicionário com listas de valores únicos
        (ordenados por primeira ocorrência) para cada chave extraída.
        """
        valores_agregados: Dict[str, List[Any]] = defaultdict(list)

        for infos_peca in self.historico:
            for chave, valor in infos_peca.items():
                valores = valor if isinstance(valor, list) else [valor]
                valores_agregados[chave].extend(valores)

        # Remove duplicatas preservando a ordem com dict.fromkeys
        self.historico = {
            chave: list(dict.fromkeys(valores))
            for chave, valores in valores_agregados.items()
        }
    