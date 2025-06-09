import streamlit as st
import os
from agentes.agente_ingestao import AgenteIngestao
from agentes.agente_analise import AgenteAnalise
from agentes.agente_memoria import AgenteMemoria
from agentes.agente_contexto import AgenteContexto
from agentes.agente_proposicao import AgenteProposicao

from agentes.orquestrador import Orquestrador

# Variáveis de sessão
if "pecas" not in st.session_state:
    st.session_state.pecas = []
if "estrutura" not in st.session_state:
    st.session_state.estrutura = {}
if "resumos" not in st.session_state:
    st.session_state.resumos = {}
if "memoria" not in st.session_state:
    st.session_state.memoria = AgenteMemoria()
if "linha_tempo" not in st.session_state:
    st.session_state.linha_tempo = []
if "narrativa" not in st.session_state:
    st.session_state.narrativa = ""
if "ato" not in st.session_state:
    st.session_state.ato = ""

st.header("🧠 InstruiAI - Assistente Processual (PoC)")

st.sidebar.title("🔧 Ações do Assistente")

# Caminho do diretório com as peças
caminho = st.sidebar.text_input("📁 Pasta com peças do processo", "data/pecas_prestacao_contas")

# 1. Ingestão
if st.sidebar.button("Executar Ingestão"):
    ingestao = AgenteIngestao()
    processo = ingestao.executar(caminho)

    st.session_state.pecas = processo["peças"]
    st.success(f"{len(st.session_state.pecas)} peça(s) carregadas.")

# Mostrar arquivos carregados
if st.session_state.pecas:
    st.subheader("🧾 Peças Carregadas")
    for p in st.session_state.pecas:
        st.markdown(f"- **{p['arquivo']}**")

# 2. Análise
if st.sidebar.button("Executar Análise"):
    analise = AgenteAnalise()
    for peca in st.session_state.pecas:
        infos, resumo = analise.executar(peca)
        st.session_state.estrutura[peca['arquivo']] = infos
        st.session_state.resumos[peca['arquivo']] = resumo
    st.success("Análise concluída.")

# 3. Memória
if st.sidebar.button("Executar Memória"):
    st.session_state.memoria.limpar_historico()
    for peca in st.session_state.pecas:
        peca_id = peca["arquivo"]
        dados = st.session_state.estrutura.get(peca_id, {})
        resumo = st.session_state.resumos.get(peca_id, "")
        st.session_state.memoria.adicionar(peca_id, dados, resumo)
    st.success("Histórico de memória atualizado.")

# 4. Contexto
if st.sidebar.button("Executar Contexto"):
    contexto = AgenteContexto(st.session_state.memoria)
    hist = st.session_state.memoria.obter_historico()
    st.session_state.linha_tempo = contexto.gerar_linha_do_tempo(hist)
    st.session_state.narrativa = contexto.gerar_resumo_narrativo(hist)
    st.success("Contexto gerado.")

# 5. Proposição
if st.sidebar.button("Executar Proposição"):
    proposicao = AgenteProposicao()
    st.session_state.ato = proposicao.executar(
        perfil_usuario="técnico",
        tipo_ato="despacho_instrucao",
        resumo=st.session_state.narrativa
    )
    st.success("Proposta de ato gerada.")

# RESULTADOS
if st.session_state.estrutura:
    st.subheader("📊 Análise") 

    with st.expander("🔍 Estrutura das Peças (NER, PII, etc.)"):
        for arquivo, estrutura in st.session_state.estrutura.items():
            st.markdown(f"**{arquivo}**")
            st.json(estrutura)

    with st.expander("🧾 Resumos das Peças"):
        for arquivo, resumo in st.session_state.resumos.items():
            st.markdown(f"**{arquivo}**")
            st.markdown(resumo)

if st.session_state.memoria:
    with st.expander("📚 Histórico da Memória"):
        for evento in st.session_state.memoria.obter_historico():
            st.markdown(f"**{evento['peca']}** - {evento['timestamp']}")
            st.json(evento["dados"])
            st.markdown(f"*Resumo:* {evento['resumo']}")

if st.session_state.linha_tempo and st.session_state.narrativa:
    st.markdown(" ### 📅 Contexto")
    with st.expander("🕒 Linha do Tempo"):
        for item in st.session_state.linha_tempo:
            st.markdown(f"- {item['data']} | **{item['peca']}** | {item['partes']}")
            st.markdown(f"  > {item['descricao']}")

    with st.expander("📝 Resumo Narrativo"):
        st.markdown(st.session_state.narrativa)

if st.session_state.ato:
    st.markdown(" ### 📄 Resultado")
    with st.expander("📄 Ato Gerado"):
        st.markdown(st.session_state.ato)
