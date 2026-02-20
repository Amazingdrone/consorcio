import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io

# Configuração da página
st.set_page_config(page_title="Tabela Sr. Jean", layout="wide")

# Função para limpar e converter valores monetários
def clean_currency(x):
    if pd.isna(x): return 0.0
    if isinstance(x, (int, float)): return float(x)
    x = str(x).replace('R$', '').replace('%', '').strip().replace('.', '').replace(',', '.')
    try: return float(x)
    except: return 0.0

# Cabeçalho VIP
st.markdown(f"# ☕ Bom dia, Sr. Jean, tudo bem?")
st.markdown(f"### Tabela atualizada do dia!")

# Upload do arquivo que o senhor baixou
uploaded_file = st.file_uploader("Arraste aqui a tabela 'Como Vem'", type=['csv', 'xlsx'])

if uploaded_file:
    try:
        # Lê o arquivo
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, sep=';', encoding='latin1')
        else:
            df = pd.read_excel(uploaded_file)
            
        if 'Codigo' in df.columns: df = df.rename(columns={'Codigo': 'Código'})

        # Realiza os cálculos matemáticos
        c = df['Credito R$'].apply(clean_currency)
        e = df['Entrada R$'].apply(clean_currency)
        p = pd.to_numeric(df['Parcelas'], errors='coerce').fillna(0)
        v = df['Valor das Parcelas'].apply(clean_currency)
        
        df['Total das parcelas_num'] = p * v
        df['Custo Total_num'] = df['Total das parcelas_num'] + e
        df['% Entrada_num'] = (e / c) * 100
        df['% Total_num'] = ((df['Custo Total_num'] - c) / c) * 100

        # Monta a tabela "Como Tem Que Ficar"
        f = pd.DataFrame()
        f['Código'] = df['Código']
        f['Segmento'] = df['Segmento'].astype(str).str.replace('Veiculos', 'Veículos')
        f['Administradora'] = df['Administradora']
        f['Crédito R$'] = c.apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['Entrada R$'] = e.apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['% Entrada'] = df['% Entrada_num'].apply(lambda x: f"{x:,.2f}%".replace(".", ","))
        f['Parcelas'] = p.astype(int)
        f['Valor das Parcelas'] = v.apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['Total das parcelas'] = df['Total das parcelas_num'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['Custo Total'] = df['Custo Total_num'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['% Total'] = df['% Total_num'].apply(lambda x: f"{x:,.2f}%".replace(".", ","))

        st.success("Tabela processada com sucesso!")
        st.dataframe(f, use_container_width=True, height=500)

        # Preparar download para Excel
        data_arq = datetime.now().strftime('%d_%m_%Y')
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            f.to_excel(writer, index=False)
        
        st.download_button(
            label="📥 BAIXAR EXCEL PRONTO",
            data=output.getvalue(),
            file_name=f"TABELA_{data_arq}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
