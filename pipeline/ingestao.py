import fitz  # PyMuPDF
from pathlib import Path

def classificar_peca(texto, filename):
    texto_lower = texto.lower()
    if "prestação de contas" in texto_lower:
        return "Relatório de Prestação de Contas", "Prefeitura"
    elif "controle interno" in texto_lower:
        return "Relatório do Controle Interno", "Controle Interno Municipal"
    elif "parecer técnico" in texto_lower:
        return "Parecer Técnico", "TCE"
    elif "notifica-se" in texto_lower:
        return "Notificação para Contrarrazões", "TCE"
    elif "defesa" in texto_lower or "prefeito" in texto_lower:
        return "Petição de Defesa", "Prefeito"
    else:
        return "Peça Não Identificada", "Desconhecido"

def processar_pecas(pdf_dir: str | Path) -> dict:
    pdf_dir = Path(pdf_dir)
    pecas_processadas = []

    for pdf_file in sorted(pdf_dir.glob("*.pdf")):
        with fitz.open(pdf_file) as doc:
            texto = "\n".join([page.get_text() for page in doc])
            tipo, origem = classificar_peca(texto, pdf_file.name)
            pecas_processadas.append({
                "tipo": tipo,
                "origem": origem,
                "arquivo": pdf_file.name,
                "texto": texto.strip()
            })

    return {
        "processo": "Prestação de Contas 2023 - Santo Vale",
        "peças": pecas_processadas
    }