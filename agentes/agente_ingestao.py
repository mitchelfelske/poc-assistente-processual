import fitz
from pathlib import Path

class AgenteIngestao():
    pecas_processadas = []

    def executar_upload(self, arquivos_pdf):
        for arquivo in arquivos_pdf:
            doc = fitz.open(stream=arquivo.read(), filetype="pdf")
            texto = "".join([pagina.get_text() for pagina in doc])
            self.pecas_processadas.append({
                "arquivo": arquivo.name,
                "texto": texto
            })
        return {"peças": self.pecas_processadas}

    def executar_local(self, caminho_pdfs: str | Path) -> dict:
        caminho_pdfs = Path(caminho_pdfs)

        for pdf_file in sorted(caminho_pdfs.glob("*.pdf")):
            with fitz.open(pdf_file) as doc:
                texto = "\n".join([page.get_text() for page in doc])
                self.pecas_processadas.append({
                        "arquivo": pdf_file.name,
                        "texto": texto.strip()
                    })
        return { "peças": self.pecas_processadas}
