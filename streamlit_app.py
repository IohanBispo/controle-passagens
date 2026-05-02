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

# --- BARRA LATERAL (ONDE VOCÊ EDITA O SALDO E PREÇO) ---
st.sidebar.header("⚙️ Painel de Controle")

# Campo para editar o Preço
preco_vigo = st.sidebar.number_input("Preço da Passagem (R$)", value=5.00, step=0.05)

st.sidebar.divider()

# Campo para Adicionar Recarga (Edita o saldo somando)
st.sidebar.subheader("💰 Adicionar Recarga")
valor_recarga = st.sidebar.number_input("Valor da Recarga (R$)", min_value=0.0, step=10.0)

if st.sidebar.button("Confirmar Recarga"):
    st.session_state.saldo += valor_recarga
    st.session_state.historico.append({
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Tipo": "Recarga",
        "Valor": f"R$ {valor_recarga:.2f}",
        "Saldo": f"R$ {st.session_state.saldo:.2f}"
    })
    st.sidebar.success("Saldo Atualizado!")

# --- PAINEL PRINCIPAL ---
st.title("🚌 Controle de Passagens")

col1, col2 = st.columns(2)
with col1:
    st.metric("Saldo Atual", f"R$ {st.session_state.saldo:.2f}")
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
        st.success("Uso registrado!")
    else:
        st.error("Saldo insuficiente!")

# EXIBIR HISTÓRICO
if st.session_state.historico:
    with st.expander("Ver Histórico Completo"):
        st.table(pd.DataFrame(st.session_state.historico).iloc[::-1])
