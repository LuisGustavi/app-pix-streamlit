import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode
from io import BytesIO

# Google Sheets
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import json

# CONFIGURAÇÕES
valor_fixo = "R$ 30,00"
codigo_pix_fixo = "00020126330014br.gov.bcb.pix011102453921142520400005303986540530.005802BR5925LUIS GUSTAVO BARBIERI KEH6010MEDIANEIRA62070503***6304436D"  # <- coloque seu código real aqui
url_planilha = "https://docs.google.com/spreadsheets/d/10xOBmlcaesiwG4G_SD6BZ_l6D2y1Kj_BbtDpTbRKWkg/edit?usp=sharing"  # <- substitua pelo link real da sua planilha

# CONFIG STREAMLIT
st.set_page_config(page_title="Pagamento Liga BT", page_icon="💸")
st.title("💸 Pagamento Liga BT")
st.markdown("Preencha seu nome abaixo para ver o QR Code de pagamento.")

# FORMULÁRIO
with st.form("formulario"):
    nome = st.text_input("Seu nome")
    enviar = st.form_submit_button("Avançar")

if enviar:
    if not nome:
        st.warning("Por favor, digite seu nome.")
    else:
        # Dados a registrar
        dados = {
            "nome": nome,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "valor": valor_fixo
        }

        # Criar DataFrame
        df = pd.DataFrame([dados])

        # Salvar no Google Sheets
        try:
            # Carregar credenciais do Streamlit Secrets
            creds_dict = json.loads(st.secrets["CREDENTIALS_JSON"])
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)

            planilha = client.open_by_url(url_planilha)
            aba = planilha.sheet1

            # Pegar dados antigos (se houver)
            dados_atuais = pd.DataFrame(aba.get_all_records())
            df_completo = pd.concat([dados_atuais, df], ignore_index=True)

            # Atualizar a planilha com os dados novos
            aba.clear()
            set_with_dataframe(aba, df_completo)

            st.success("Dados enviados com sucesso para o Google Sheets! ✅")

        except Exception as e:
            st.error(f"Erro ao salvar no Google Sheets: {e}")

        # Gerar QR Code
        qr_img = qrcode.make(codigo_pix_fixo)
        buffer = BytesIO()
        qr_img.save(buffer)

        st.image(buffer.getvalue(), caption="Escaneie para pagar via Pix", width=300)
        st.code(codigo_pix_fixo, language="text")
