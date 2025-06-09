# Assistente Processual (PoC)

Este projeto é uma prova de conceito para um assistente processual multiagente na área jurídica. Esta versão faz a ingestão, resumo e extração de informações de peças processuais em PDF.

## Estrutura

- `pipeline/ingestao.py`: código de leitura e classificação de PDFs
- `pipeline/analise.py`: resumo e extração com Azure OpenAI
- `pipeline/proposicao.py`: Propõe ato conforme perfil do usuário, tipo de ato, resumo de peças e informações do processo
- `main.py`: executa o pipeline completo
- `data/pecas_prestacao_contas/`: PDFs simulados

## Como executar

1. Configure seu arquivo `.env` com as chaves do Azure OpenAI:

```
AZURE_OPENAI_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

2. Instale os requisitos:

```bash
pip install -r requirements.txt
```

### Execute o pipeline
3. Pela linha de comando:

```bash
python main.py
```

3. Pela interface (streamlit):

```bash
streamlit run app.py
```

Acesse a URL: http://localhost:8501
