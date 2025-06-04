from pathlib import Path
from jinja2 import Template

from agentes.interface_agente import AgenteInterface

class AgenteProposicao(AgenteInterface):
    def carregar_template(self, tipo_ato: str) -> Template:
        caminho = Path("templates") / f"{tipo_ato}.txt"
        with open(caminho, encoding="utf-8") as f:
            return Template(f.read())

    def gerar_ato(self, perfil_usuario: str, tipo_ato: str, resumo: str) -> str:
        template = self.carregar_template(tipo_ato)
        return template.render(perfil=perfil_usuario, resumo=resumo)

    def executar(self, perfil_usuario: str, tipo_ato: str, resumo: str) -> str:
        return self.gerar_ato(perfil_usuario, tipo_ato, resumo)
