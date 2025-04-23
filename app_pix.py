import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Pagamento via Pix", page_icon="💸")

st.title("💸 Pagamento via Pix")
st.markdown("Preencha seu nome abaixo para ver o QR Code de pagamento.")

# Formulário
with st.form("formulario"):
    nome = st.text_input("Seu nome")
    enviar = st.form_submit_button("Avançar")

if enviar:
    if not nome:
        st.warning("Por favor, digite seu nome.")
    else:
        valor_fixo = "R$ 30,00"  # <- Troque aqui se quiser alterar o valor exibido

        dados = {
            "nome": nome,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "valor": valor_fixo
        }

        try:
            df = pd.read_csv("dados_pagamentos.csv")
            df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
        except FileNotFoundError:
            df = pd.DataFrame([dados])

        df.to_csv("dados_pagamentos.csv", index=False)

        st.success("Dados salvos com sucesso!")

        # Exibir o QR Code fixo (imagem gerada previamente)
        st.image("qr_code.png", caption="Escaneie para pagar via Pix", width=300)
