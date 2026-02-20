import os
import requests
import pandas as pd
import numpy as np

# Pasta onde o arquivo será salvo
PASTA_ATUAL = os.path.abspath(os.path.dirname(__file__))

def clean_currency(x):
    if pd.isna(x): return np.nan
    if isinstance(x, (int, float)): return float(x)
    x = str(x).replace('R$', '').replace('%', '').strip().replace('.', '').replace(',', '.')
    try: return float(x)
    except: return np.nan

def processar_e_salvar(caminho_input):
    print("Processando os dados matemáticos...")
    # Tenta ler o CSV que o site envia
    try:
        df = pd.read_csv(caminho_input, sep=';', encoding='latin1')
    except:
        df = pd.read_csv(caminho_input, sep=';', encoding='utf-8')

    if 'Codigo' in df.columns: df = df.rename(columns={'Codigo': 'Código'})

    # Cálculos
    df['Crédito Num'] = df['Credito R$'].apply(clean_currency)
    df['Entrada Num'] = df['Entrada R$'].apply(clean_currency)
    df['Parcelas Num'] = pd.to_numeric(df['Parcelas'], errors='coerce')
    df['Valor Parcela Num'] = df['Valor das Parcelas'].apply(clean_currency)
    
    df['Total das parcelas'] = df['Parcelas Num'] * df['Valor Parcela Num']
    df['Custo Total'] = df['Total das parcelas'] + df['Entrada Num']
    df['% Entrada'] = (df['Entrada Num'] / df['Crédito Num']) * 100
    df['% Total'] = ((df['Custo Total'] - df['Crédito Num']) / df['Crédito Num']) * 100

    # Montagem da tabela final
    df_final = pd.DataFrame()
    df_final['Código'] = df['Código']
    df_final['Segmento'] = df['Segmento'].astype(str).str.replace('Veiculos', 'Veículos')
    df_final['Administradora'] = df['Administradora']
    df_final['Crédito R$'] = df['Crédito Num'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df_final['Entrada R$'] = df['Entrada Num'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df_final['% Entrada'] = df['% Entrada'].apply(lambda x: f"{x:,.2f}%".replace(".", ","))
    df_final['Parcelas'] = df['Parcelas Num'].fillna(0).astype(int)
    df_final['Valor das Parcelas'] = df['Valor Parcela Num'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df_final['Total das parcelas'] = df['Total das parcelas'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df_final['Custo Total'] = df['Custo Total'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df_final['% Total'] = df['% Total'].apply(lambda x: f"{x:,.2f}%".replace(".", ","))

    caminho_saida = os.path.join(PASTA_ATUAL, "tabela_do_dia.xlsx")
    df_final.to_excel(caminho_saida, index=False)
    print(f"Arquivo final gerado com sucesso: {caminho_saida}")

def executar_robot():
    # URL direta do download que o botão aciona
    url_download = "https://cartascontempladas.com.br/wp-admin/admin-ajax.php?action=gerar_csv_cartas"
    
    # Fingindo ser um navegador real para o site não bloquear
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("Solicitando arquivo diretamente ao servidor...")
    resposta = requests.get(url_download, headers=headers)

    if resposta.status_code == 200:
        caminho_temp = os.path.join(PASTA_ATUAL, "temp_data.csv")
        with open(caminho_temp, 'wb') as f:
            f.write(resposta.content)
        
        processar_e_salvar(caminho_temp)
        os.remove(caminho_temp)
    else:
        print(f"Erro ao baixar: Status {resposta.status_code}")
        # Cria um arquivo vazio para o Git não dar erro caso o download falhe
        pd.DataFrame().to_excel(os.path.join(PASTA_ATUAL, "tabela_do_dia.xlsx"))

if __name__ == "__main__":
    executar_robot()
