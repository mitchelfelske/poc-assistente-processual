# Assistente Processual (PoC)

Este projeto é uma prova de conceito para um assistente processual multiagente na área jurídica. Esta versão faz a ingestão e classificação automática de peças processuais em PDF.

## Estrutura

- `pipeline/ingestao.py`: código de leitura e classificação de PDFs
- `main.py`: executa o pipeline de ingestão
- `data/pecas_prestacao_contas/`: PDFs simulados

## Como executar

```bash
pip install -r requirements.txt
python main.py
```