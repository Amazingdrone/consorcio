import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuração da página (deve ser a primeira linha)
st.set_page_config(page_title="Tabela de Cartas - Sr. Jean", layout="wide")

# 2. Saudação personalizada conforme solicitado
st.markdown(f"## ☕ Bom dia, Sr. Jean, tudo bem? - Tabela atualizada do dia!")

# 3. Definição de nomes e datas
data_atual = datetime.now()
data_formatada = data_atual.strftime('%d/%m/%Y')
nome_arquivo_download = data_atual.strftime('TABELA_%d_%m_%Y.xlsx')

# Caminho do arquivo gerado pelo robô
CAMINHO_ARQUIVO = "tabela_do_dia.xlsx"

# 4. Lógica de exibição da tabela
if os.path.exists(CAMINHO_ARQUIVO):
    try:
        # Forçamos o pandas a ler o arquivo sem usar cache do Streamlit
        df = pd.read_excel(CAMINHO_ARQUIVO, engine='openpyxl')
        
        if not df.empty:
            st.write(f"Exibindo dados atualizados em: **{data_formatada}**")
            
            # Exibe a tabela com altura ajustada para não sumir
            st.dataframe(
                df, 
                use_container_width=True, 
                height=500
            )
            
            st.markdown("---")
            
            # 5. Botão de Download com o nome solicitado: TABELA_DATA.xlsx
            with open(CAMINHO_ARQUIVO, "rb") as file:
                st.download_button(
                    label="📥 BAIXAR TABELA PARA EXCEL",
                    data=file,
                    file_name=nome_arquivo_download,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("Sr. Jean, o arquivo foi encontrado, mas parece estar vazio. Por favor, verifique o robô.")
            
    except Exception as e:
        st.error(f"Erro técnico ao carregar a tabela: {e}")
else:
    # Se o arquivo não existe, mostramos o erro de forma clara
    st.error(f"❌ Sr. Jean, o arquivo '{CAMINHO_ARQUIVO}' não foi encontrado no servidor.")
    st.info("Aguarde o robô rodar às 08h ou execute-o manualmente no GitHub Actions.")

# Rodapé simples
st.caption(f"Sistema de Monitoramento Automático - Atualizado em {data_formatada}")
