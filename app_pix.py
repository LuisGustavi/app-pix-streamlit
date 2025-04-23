import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode
from io import BytesIO

# CONFIG DO APP
st.set_page_config(page_title="Pagamento via Pix", page_icon="💸")

st.title("💸 Pagamento via Pix")
st.markdown("Preencha o nome abaixo para continuar com o pagamento.")

# FORMULÁRIO
with st.form("formulario"):
    nome = st.text_input("Seu nome")
    enviar = st.form_submit_button("Avançar")

if enviar:
if not nome:
    st.warning("Por favor, digite seu nome.")
else:
    valor_fixo = "R$ 30,00"  # <- troque aqui pelo valor real do seu QR Code

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

    # Exibir o QR Code (que você já tem salvo como imagem)
    st.image("qr_code.png", caption="Escaneie para pagar via Pix", width=300)



        try:
            df = pd.read_csv("dados_pagamentos.csv")
            df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
        except FileNotFoundError:
            df = pd.DataFrame([dados])

        df.to_csv("dados_pagamentos.csv", index=False)
        st.success("Dados salvos com sucesso!")

        # QR CODE FIXO (que você já tem no seu app)
        codigo_pix_fixo = "00020126330014br.gov.bcb.pix011102453921142520400005303986540530.005802BR5925LUIS GUSTAVO BARBIERI KEH6010MEDIANEIRA62070503***6304436D"

        # Gerar imagem do QR Code em memória
        qr = qrcode.make(codigo_pix_fixo)
        buffer = BytesIO()
        qr.save(buffer)
        buffer.seek(0)

        st.image(buffer, caption="Escaneie para pagar via Pix", width=300)
        st.code(codigo_pix_fixo, language="text")
