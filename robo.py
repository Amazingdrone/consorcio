import os
import requests
import pandas as pd
import numpy as np

PASTA = os.path.abspath(os.path.dirname(__file__))

def clean_currency(x):
    if pd.isna(x): return np.nan
    x = str(x).replace('R$', '').replace('%', '').strip().replace('.', '').replace(',', '.')
    try: return float(x)
    except: return np.nan

def executar():
    url = "https://cartascontempladas.com.br/wp-admin/admin-ajax.php?action=gerar_csv_cartas"
    
    # DISFARCE COMPLETO: Imita um navegador Chrome real acessando o site
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://cartascontempladas.com.br/ver-todas-as-cartas-contempladas/",
        "X-Requested-With": "XMLHttpRequest"
    }

    print("Buscando dados no servidor do site...")
    res = requests.get(url, headers=headers)

    if res.status_code == 200 and len(res.content) > 100:
        temp = os.path.join(PASTA, "temp.csv")
        with open(temp, 'wb') as f:
            f.write(res.content)
        
        # Processamento
        try:
            df = pd.read_csv(temp, sep=';', encoding='latin1')
        except:
            df = pd.read_csv(temp, sep=';', encoding='utf-8')

        if 'Codigo' in df.columns: df = df.rename(columns={'Codigo': 'Código'})

        # Matemática das Colunas
        df['c'] = df['Credito R$'].apply(clean_currency)
        df['e'] = df['Entrada R$'].apply(clean_currency)
        df['p'] = pd.to_numeric(df['Parcelas'], errors='coerce')
        df['v'] = df['Valor das Parcelas'].apply(clean_currency)
        
        df['Total das parcelas'] = df['p'] * df['v']
        df['Custo Total'] = df['Total das parcelas'] + df['e']
        df['% Entrada'] = (df['e'] / df['c']) * 100
        df['% Total'] = ((df['Custo Total'] - df['c']) / df['c']) * 100

        # Montagem Final
        f = pd.DataFrame()
        f['Código'] = df['Código']
        f['Segmento'] = df['Segmento'].astype(str).str.replace('Veiculos', 'Veículos')
        f['Administradora'] = df['Administradora']
        f['Crédito R$'] = df['c'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['Entrada R$'] = df['e'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['% Entrada'] = df['% Entrada'].apply(lambda x: f"{x:,.2f}%".replace(".", ","))
        f['Parcelas'] = df['p'].fillna(0).astype(int)
        f['Valor das Parcelas'] = df['v'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['Total das parcelas'] = df['Total das parcelas'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['Custo Total'] = df['Custo Total'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        f['% Total'] = df['% Total'].apply(lambda x: f"{x:,.2f}%".replace(".", ","))

        f.to_excel(os.path.join(PASTA, "tabela_do_dia.xlsx"), index=False)
        print("Tabela gerada com sucesso!")
        os.remove(temp)
    else:
        print("ERRO: O site negou o acesso ou enviou arquivo vazio.")
        # Se falhar, NÃO cria o excel para o GitHub acusar erro e a gente saber
        if os.path.exists(os.path.join(PASTA, "tabela_do_dia.xlsx")):
            os.remove(os.path.join(PASTA, "tabela_do_dia.xlsx"))

if __name__ == "__main__":
    executar()
