import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode
from io import BytesIO

st.set_page_config(page_title="Pagamento Liga BT Medianeira", page_icon="💸")

st.title("💸 Pagamento Liga BT Medianeira")
st.markdown("Preencha seu nome abaixo para ver o QR Code de pagamento.")

# Formulário
with st.form("formulario"):
    nome = st.text_input("Seu nome")
    enviar = st.form_submit_button("Avançar")

if enviar:
    if not nome:
        st.warning("Por favor, digite seu nome.")
    else:
        valor_fixo = "R$ 30,00"  # <- valor associado ao QR Code fixo
        codigo_pix_fixo = "00020126330014br.gov.bcb.pix011102453921142520400005303986540530.005802BR5925LUIS GUSTAVO BARBIERI KEH6010MEDIANEIRA62070503***6304436D"  # <- substitua por seu código real

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

        # Gerar QR Code a partir do código fixo
        qr_img = qrcode.make(codigo_pix_fixo)
        buffer = BytesIO()
        qr_img.save(buffer)

        st.image(buffer.getvalue(), caption="Escaneie para pagar via Pix", width=300)
        st.code(codigo_pix_fixo, language="text")
