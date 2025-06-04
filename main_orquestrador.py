from agentes.orquestrador import Orquestrador

if __name__ == "__main__":
    orquestrador = Orquestrador()

    resumo =  """
        O "Relatório de Prestação de Contas - Exercício 2023" da Prefeitura Municipal de Santo Vale apresenta as demonstrações contábeis, orçamentárias e financeiras do município. Destaca um superávit financeiro de R$ 2.300.000,00 e o cumprimento dos limites constitucionais de gastos em saúde (16,2%) e educação (25,5%). A despesa com pessoal representa 49,5% da receita corrente líquida. O relatório inclui também o parecer do controle interno e quadros demonstrativos da execução orçamentária.

        O Relatório Técnico do Controle Interno da Prefeitura Municipal de Santo Vale identifica inconsistências na contabilização de restos a pagar não processados, totalizando R$ 920.000,00, e a falta de publicação de editais completos no Portal da Transparência para licitações de materiais escolares em junho de 2023. O documento recomenda a regularização dos lançamentos contábeis e a comprovação do procedimento licitatório. As partes envolvidas são a Prefeitura Municipal de Santo Vale e a Unidade de Controle Interno.

        O parecer técnico da Unidade de Fiscalização do Tribunal de Contas Estadual analisa as contas da Prefeitura de Santo Vale, constatando o cumprimento dos índices legais, exceto pela falta de publicação do Relatório de Gestão Fiscal do 2º semestre de 2023. Recomenda-se o julgamento com ressalvas e a aplicação de uma multa simbólica devido à falta de transparência fiscal. As partes envolvidas são a Prefeitura de Santo Vale e o Tribunal de Contas Estadual.

        A peça processual é uma notificação do Tribunal de Contas Estadual ao Executivo Municipal de Santo Vale, solicitando a apresentação de contrarrazões em um prazo de 15 dias úteis. Os pontos a serem contestados incluem inconsistências nos restos a pagar no valor de R$ 920.000,00, a falta de publicação do Relatório de Gestão Fiscal do 2º semestre e a suposta irregularidade no processo licitatório para aquisição de materiais escolares.

        A peça processual é uma petição de defesa apresentada pelo Prefeito Municipal de Santo Vale, dirigida ao Conselheiro Relator. O documento visa esclarecer questões levantadas pela unidade técnica, destacando um erro no sistema de contabilidade relacionado aos restos a pagar, já corrigido, e falhas técnicas na publicação do Relatório de Gestão Fiscal no Portal da Transparência. Além disso, anexa cópia do processo licitatório referente à compra de materiais escolares.
    """

    ato, infos, revisao = orquestrador.executar_fluxo(
        caminho_pecas="data/pecas_prestacao_contas",
        tipo_ato="técnico",
        modelo_ato="despacho_instrucao",
        resumo=resumo
    )

    print("\nAto gerado:\n")
    print(ato)
    print("\nInformações extraídas:")
    for chave, valor in infos.items():
        print(f"{chave}: {valor}")
    print("\nResultado da revisão:", revisao)
