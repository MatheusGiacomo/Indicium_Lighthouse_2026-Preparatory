import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def extract_ibge_data():
    print("Iniciando extração do IPCA (IBGE)...")

    url = "https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/-12/variaveis/63?localidades=N1[all]"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        serie_temporal = data[0]['resultados'][0]['series'][0]['serie']
        
        df = pd.DataFrame(list(serie_temporal.items()), columns=['mes_referencia', 'valor_ipca'])
        return df
    
    except Exception as e:
        print(f"Erro crítico na extração: {e}")
        return None

def transform_data(df):
    print("Transformando dados...")
    df['valor_ipca'] = pd.to_numeric(df['valor_ipca'])
    df = df.sort_values('mes_referencia', ascending=False)
    return df

def load_to_postgres(df, table_name):
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB")

    conn_str = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(conn_str)

    print(f"Carregando {len(df)} linhas na tabela {table_name}...")
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Sucesso, dados carregados.")

if __name__ == "__main__":
    df_raw = extract_ibge_data()
    if df_raw is not None:
        df_clean = transform_data(df_raw)
        load_to_postgres(df_clean, "ext_ipca_ibge")