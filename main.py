
from pipeline.ingestao import processar_pecas
from pipeline.analise import resumir_peca, extrair_informacoes
from pipeline.proposicao import gerar_ato
from pipeline.revisao import revisar_ato

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

        for chave, valor in informacoes_gerais.items():
            if isinstance(valor, list):
                informacoes_gerais[chave] = list(set(valor))
            
        print("\nResumindo peça...")    
        #resumo = resumir_peca(p["texto"])
        #resumo_geral += resumo + "\n"
        print("\n")

    print("Análise concluída.")

    resumo_geral = """
        O "Relatório de Prestação de Contas - Exercício 2023" da Prefeitura Municipal de Santo Vale apresenta as demonstrações contábeis, orçamentárias e financeiras do município. Destaca um superávit financeiro de R$ 2.300.000,00 e o cumprimento dos limites constitucionais de gastos em saúde (16,2%) e educação (25,5%). A despesa com pessoal representa 49,5% da receita corrente líquida. O relatório inclui também o parecer do controle interno e quadros demonstrativos da execução orçamentária.

        O Relatório Técnico do Controle Interno da Prefeitura Municipal de Santo Vale identifica inconsistências na contabilização de restos a pagar não processados, totalizando R$ 920.000,00, e a falta de publicação de editais completos no Portal da Transparência para licitações de materiais escolares em junho de 2023. O documento recomenda a regularização dos lançamentos contábeis e a comprovação do procedimento licitatório. As partes envolvidas são a Prefeitura Municipal de Santo Vale e a Unidade de Controle Interno.

        O parecer técnico da Unidade de Fiscalização do Tribunal de Contas Estadual analisa as contas da Prefeitura de Santo Vale, constatando o cumprimento dos índices legais, exceto pela falta de publicação do Relatório de Gestão Fiscal do 2º semestre de 2023. Recomenda-se o julgamento com ressalvas e a aplicação de uma multa simbólica devido à falta de transparência fiscal. As partes envolvidas são a Prefeitura de Santo Vale e o Tribunal de Contas Estadual.

        A peça processual é uma notificação do Tribunal de Contas Estadual ao Executivo Municipal de Santo Vale, solicitando a apresentação de contrarrazões em um prazo de 15 dias úteis. Os pontos a serem contestados incluem inconsistências nos restos a pagar no valor de R$ 920.000,00, a falta de publicação do Relatório de Gestão Fiscal do 2º semestre e a suposta irregularidade no processo licitatório para aquisição de materiais escolares.

        A peça processual é uma petição de defesa apresentada pelo Prefeito Municipal de Santo Vale, dirigida ao Conselheiro Relator. O documento visa esclarecer questões levantadas pela unidade técnica, destacando um erro no sistema de contabilidade relacionado aos restos a pagar, já corrigido, e falhas técnicas na publicação do Relatório de Gestão Fiscal no Portal da Transparência. Além disso, anexa cópia do processo licitatório referente à compra de materiais escolares.
        """

    print("\nGerando ato...")
    ato = gerar_ato(
        perfil_usuario="técnico",
        tipo_ato="despacho_instrucao",
        resumo=resumo_geral
    )
    print(ato)
    print("\nAto gerado com sucesso!")
    
    print("\nInformações gerais extraídas:")
    for chave, valor in informacoes_gerais.items():
        print(f"{chave}: {valor}")

    print("\nRevisando ato...")
    revisao = revisar_ato(ato, informacoes_gerais)
    print("Ato completo?" , revisao["completo"])
    if not revisao["completo"]:
        print("Campos faltando:", revisao["faltando"])
        print("Comentário:", revisao["comentario"])
