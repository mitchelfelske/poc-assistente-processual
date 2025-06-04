
from pipeline.ingestao import processar_pecas
from pipeline.analise import resumir_peca, extrair_informacoes
from pipeline.proposicao import gerar_ato

if __name__ == "__main__":
    caminho_pdfs = "data/pecas_prestacao_contas"
    processo = processar_pecas(caminho_pdfs)

    informacoes_gerais = {}
    resumo_geral = ""

    print("Processando peças:")
    for p in processo["peças"]:
        print(f"Processo: {processo['processo']}")
        print(f"{p['tipo']} ({p['origem']}) -> {p['arquivo']}")

        print("Analisando peça...")
        infos = extrair_informacoes(p["texto"])
        for chave, valor in infos.items():
            if chave in informacoes_gerais:
                # Se já existe, adiciona na lista (ou cria a lista)
                if isinstance(informacoes_gerais[chave], list):
                    informacoes_gerais[chave].append(valor)
                else:
                    informacoes_gerais[chave] = [informacoes_gerais[chave], valor]
            else:
                # Se não existe, cria a chave com o valor direto
                informacoes_gerais[chave] = valor
        
        print("\nResumindo peça...")    
        resumo = resumir_peca(p["texto"])
        resumo_geral += resumo + "\n"
        print("\n")

    print("Análise concluída.")

    print("\nGerando ato...")
    ato = gerar_ato(
        perfil_usuario="técnico",
        tipo_ato="despacho_instrução",
        resumo=resumo_geral,
        informacoes=informacoes_gerais
    )
    print(ato)
