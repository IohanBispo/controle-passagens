import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Meu VT Digital", page_icon="🚌")

# LINK DA SUA PLANILHA (Já configurado para leitura)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1Su5DFQQlsyStqA30YJWPsIbrFzSEva_9vnJB-vSRWIM/export?format=csv"

# FUNÇÃO PARA LER OS DADOS
def carregar_dados():
    try:
        # Lê a planilha do Google
        df = pd.read_csv(URL_PLANILHA)
        return df
    except:
        # Se der erro ou estiver vazia, cria uma base inicial
        return pd.DataFrame(columns=['Data', 'Uso', 'Saldo'])

df = carregar_dados()

# --- INTERFACE NO CELULAR ---
st.title("🚌 Controle de Passagens")

# Pegar o último saldo registrado na planilha
if not df.empty and 'Saldo' in df.columns:
    # Pega o valor da última linha da coluna Saldo
    saldo_atual = float(df['Saldo'].iloc[-1])
else:
    saldo_atual = 220.00 # Valor inicial padrão

# EXIBIR O SALDO COM DESTAQUE
st.metric("Saldo na Carteira", f"R$ {saldo_atual:.2f}")

st.divider()

# BOTÕES DE USO RÁPIDO
st.subheader("Quanto usou hoje?")
qtd = st.radio("Selecione a quantidade:", [0, 1, 2], index=2, horizontal=True)

if st.button("Confirmar e Calcular"):
    preco_passagem = 5.00 # Você pode ajustar o preço aqui
    novo_saldo = saldo_atual - (qtd * preco_passagem)
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    
    st.success(f"Cálculo feito! Se você atualizar a planilha, seu novo saldo será: R$ {novo_saldo:.2f}")
    st.balloons()
    
    # Avisar que para salvar "para sempre" precisa mexer na planilha
    st.info("💡 Como estamos no modo simples, após clicar aqui, vá na sua planilha do Google e anote o novo saldo na última linha para ele ficar salvo!")

# MOSTRAR AS ÚLTIMAS LINHAS DA PLANILHA
if not df.empty:
    with st.expander("Ver histórico da planilha"):
        st.dataframe(df.tail(10))