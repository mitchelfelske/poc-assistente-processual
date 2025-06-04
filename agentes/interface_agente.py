from abc import ABC, abstractmethod

# --- Interface base para agentes ---
class AgenteInterface(ABC):
    @abstractmethod
    def executar(self, *args, **kwargs):
        pass
