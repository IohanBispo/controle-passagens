import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu VT Pro", page_icon="🚌")

# --- INICIALIZAÇÃO DE DADOS (MEMÓRIA DO APP) ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 220.00
if 'historico' not in st.session_state:
    st.session_state.historico = []

# --- BARRA LATERAL (CONFIGURAÇÕES E RECARGA) ---
st.sidebar.header("⚙️ Configurações")

# 1. Editar valor da passagem
preco_vigo = st.sidebar.number_input("Preço da Passagem (R$)", value=5.00, step=0.05)

st.sidebar.divider()

# 2. Adicionar Recarga
st.sidebar.subheader("➕ Recarregar")
valor_recarga = st.sidebar.number_input("Valor da Recarga (R$)", min_value=0.0, step=10.0)

if st.sidebar.button("Confirmar Recarga"):
    st.session_state.saldo += valor_recarga
    # Salva no histórico
    st.session_state.historico.append({
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Tipo": "Recarga",
        "Valor": f"R$ {valor_recarga:.2f}",
        "Saldo Resultante": f"R$ {st.session_state.saldo:.2f}"
    })
    st.sidebar.success("Recarga adicionada!")

# --- PAINEL PRINCIPAL ---
st.title("🚌 Controle de Passagens")

# 3. Visualização de Saldo e Passagens Restantes
col1, col2 = st.columns(2)
with col1:
    st.metric("Saldo em Carteira", f"R$ {st.session_state.saldo:.2f}")
with col2:
    # 4. Quantidade de passagens restantes
    restantes = int(st.session_state.saldo // preco_vigo)
    st.metric("Viagens Restantes", restantes)

st.divider()

# 5. Registrar Uso
st.subheader("📍 Registrar Uso")
qtd = st.radio("Quantas passagens usou agora?", [1, 2, 3, 4], index=1, horizontal=True)

if st.button("Confirmar Uso"):
    custo_total = qtd * preco_vigo
    if st.session_state.saldo >= custo_total:
        st.session_state.saldo -= custo_total
        # Salva no histórico
        st.session_state.historico.append({
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Tipo": f"Uso ({qtd} pass)",
            "Valor": f"- R$ {custo_total:.2f}",
            "Saldo Resultante": f"R$ {st.session_state.saldo:.2f}"
        })
        st.success(f"Registrado! Saldo atual: R$ {st.session_state.saldo:.2f}")
        st.balloons()
    else:
        st.error("Saldo insuficiente!")

# --- 6. HISTÓRICOS ---
st.divider()
aba_uso, aba_recarga = st.tabs(["📊 Histórico de Uso", "💰 Histórico de Recargas"])

with aba_uso:
    if st.session_state.historico:
        df_uso = pd.DataFrame(st.session_state.historico)
        # Filtra apenas o que não é recarga
        df_uso = df_uso[df_uso['Tipo'].str.contains("Uso")]
        st.table(df_uso.iloc[::-1]) # Mostra os mais novos primeiro
    else:
        st.write("Nenhum uso registrado.")

with aba_recarga:
    if st.session_state.historico:
        df_rec = pd.DataFrame(st.session_state.historico)
        # Filtra apenas recargas
        df_rec = df_rec[df_rec['Tipo'] == "Recarga"]
        st.table(df_rec.iloc[::-1])
    else:
        st.write("Nenhuma recarga registrada.")
