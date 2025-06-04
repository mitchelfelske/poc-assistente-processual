from pathlib import Path

from agentes.interface_agente import AgenteInterface

class AgenteIngestao(AgenteInterface):
    def classificar_peca(self, texto):
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

    def executar(self, caminho_pdfs: str | Path) -> dict:
        import fitz  # PyMuPDF
        caminho_pdfs = Path(caminho_pdfs)
        pecas_processadas = []

        for pdf_file in sorted(caminho_pdfs.glob("*.pdf")):
            with fitz.open(pdf_file) as doc:
                texto = "\n".join([page.get_text() for page in doc])
                tipo, origem = self.classificar_peca(texto)
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
