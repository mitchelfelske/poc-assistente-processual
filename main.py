from pipeline.ingestao import processar_pecas

if __name__ == "__main__":
    caminho_pdfs = "data/pecas_prestacao_contas"
    processo = processar_pecas(caminho_pdfs)

    for p in processo["peças"]:
        print(f"{p['tipo']} ({p['origem']}) -> {p['arquivo']}\n {p['texto']}\n")