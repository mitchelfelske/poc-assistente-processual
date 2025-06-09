from agentes.orquestrador import Orquestrador

if __name__ == "__main__":
    orquestrador = Orquestrador()

    linha_tempo, resumo_narrativo, ato = orquestrador.executar_fluxo(
        caminho_pecas="data/pecas_prestacao_contas",
        tipo_ato="técnico",
        modelo_ato="despacho_instrucao"
    )

    print("\nAto gerado:\n")
    print(ato)
    print("\nLinha do Tempo:")
    print("\n".join(f"{evento['data']}: {evento['peca']} - {evento['partes']} - {evento['descricao']}" for evento in linha_tempo))
    print("\nResumo Narrativo:")
    print(resumo_narrativo)
