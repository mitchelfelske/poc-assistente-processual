
from jinja2 import Template
from pathlib import Path

def carregar_template(tipo_ato: str) -> Template:
    """Carrega o template de ato com base no tipo."""
    caminho = Path("templates") / f"{tipo_ato}.txt"
    with open(caminho, encoding="utf-8") as f:
        return Template(f.read())

def gerar_ato(perfil_usuario: str, tipo_ato: str, resumo: str) -> str:
    """Gera a minuta do ato processual."""
    template = carregar_template(tipo_ato)
    return template.render(perfil=perfil_usuario, resumo=resumo)
