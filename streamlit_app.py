import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu VT Pro", page_icon="🚌")

# --- INICIALIZAÇÃO DE DADOS ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 220.00
if 'historico' not in st.session_state:
    st.session_state.historico = []

# --- PAINEL PRINCIPAL ---
st.title("🚌 Controle de Passagens")

# DEFINIÇÃO DO PREÇO (Pode ser alterado na barra lateral)
preco_vigo = st.sidebar.number_input("Preço da Passagem (R$)", value=5.00, step=0.05)

# BLOCO DE DESTAQUE (Igual à image_9502fd.png)
col1, col2 = st.columns(2)

with col1:
    # Mantém o visual que você gosta
    st.metric("Saldo Atual", f"R$ {st.session_state.saldo:.2f}")
    # ADICIONA A FUNÇÃO DE EDITAR LOGO ABAIXO DO DESTAQUE
    novo_saldo_manual = st.number_input("Editar Saldo Manualmente", value=float(st.session_state.saldo), step=1.0, label_visibility="collapsed")
    if novo_saldo_manual != st.session_state.saldo:
        st.session_state.saldo = novo_saldo_manual
        st.rerun()

with col2:
    restantes = int(st.session_state.saldo // preco_vigo)
    st.metric("Viagens Restantes", restantes)

st.divider()

# REGISTRAR USO
st.subheader("📍 Registrar Uso")
qtd = st.radio("Quantas passagens usou?", [1, 2, 3, 4], index=1, horizontal=True)

if st.button("Confirmar e Descontar"):
    custo = qtd * preco_vigo
    if st.session_state.saldo >= custo:
        st.session_state.saldo -= custo
        st.session_state.historico.append({
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Tipo": f"Uso ({qtd} pass)",
            "Valor": f"- R$ {custo:.2f}",
            "Saldo": f"R$ {st.session_state.saldo:.2f}"
        })
        st.rerun()
    else:
        st.error("Saldo insuficiente!")

# EXIBIR HISTÓRICO
if st.session_state.historico:
    with st.expander("Ver Histórico"):
        st.table(pd.DataFrame(st.session_state.historico).iloc[::-1])
