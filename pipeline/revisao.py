
def revisar_ato(ato: str, dados_extraidos: dict) -> dict:
    """Valida se o ato está consistente com os dados extraídos."""
    resultado = {
        "completo": True,
        "faltando": [],
        "comentario": ""
    }

    for chave, valores in dados_extraidos.items():
        if not isinstance(valores, list):
            valores = [valores]

        for valor in valores:
            print(f"Verificando valor: {valor}")
            if valor not in ato:
                resultado["completo"] = False
                resultado["faltando"].append({chave: valor})

    if not resultado["completo"]:
        resultado["comentario"] = "Algumas informações extraídas não foram utilizadas no ato."

    return resultado
