import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Tabela Sr. Jean", layout="wide")

# Pegar a data atual para o título e nome do arquivo
data_hoje = datetime.now().strftime('%d/%m/%Y')
data_arquivo = datetime.now().strftime('%d_%m_%Y')

# Cabeçalho personalizado
st.title(f"☕ Bom dia, Sr. Jean, tudo bem?")
st.subheader(f"Tabela atualizada do dia {data_hoje}!")

arquivo_pronto = "tabela_do_dia.xlsx"

# Verifica se o arquivo existe
if os.path.exists(arquivo_pronto):
    try:
        # Carrega os dados
        df_final = pd.read_excel(arquivo_pronto)
        
        # Garante que a tabela apareça na tela com largura total
        st.write("### Confira as oportunidades de hoje:")
        st.dataframe(df_final, use_container_width=True, height=600)
        
        # Espaço extra
        st.markdown("---")
        
        # Botão de Download com nome dinâmico (TABELA_DD_MM_AAAA.xlsx)
        with open(arquivo_pronto, "rb") as file:
            st.download_button(
                label=f"📥 BAIXAR TABELA ({data_hoje})",
                data=file,
                file_name=f"TABELA_{data_arquivo}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    except Exception as e:
        st.error(f"Sr. Jean, houve um erro ao ler os dados: {e}")
else:
    # Caso o robô ainda não tenha rodado ou o arquivo não esteja na pasta
    st.warning(f"Sr. Jean, a tabela do dia {data_hoje} ainda não foi gerada. Por favor, verifique se o robô rodou às 08h.")
    st.info("Se você acabou de configurar, vá no GitHub e aperte 'Run Workflow' para gerar a primeira tabela.")
