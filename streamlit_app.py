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

# 1. MOSTRADOR (O que você vê destacado na imagem image_9502fd.png)
col1, col2 = st.columns(2)
with col1:
    st.metric("Saldo Atual", f"R$ {st.session_state.saldo:.2f}")
with col2:
    # Preço padrão para o cálculo das passagens restantes
    preco_vigo = 5.00 
    restantes = int(st.session_state.saldo // preco_vigo)
    st.metric("Viagens Restantes", restantes)

st.divider()

# 2. ÁREA DE EDIÇÃO DIRETA (Para mudar o que está destacado acima)
with st.expander("📝 Editar Saldo ou Preço Manualmente"):
    # Se você mudar aqui, o destaque lá em cima muda na mesma hora!
    novo_val = st.number_input("Alterar valor total para:", value=float(st.session_state.saldo), step=1.0)
    if novo_val != st.session_state.saldo:
        st.session_state.saldo = novo_val
        st.rerun()

st.divider()

# 3. REGISTRAR USO RÁPIDO
st.subheader("📍 Marcar Uso")
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

# HISTÓRICO
if st.session_state.historico:
    with st.expander("📋 Ver Histórico"):
        st.table(pd.DataFrame(st.session_state.historico).iloc[::-1])
