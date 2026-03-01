import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class GovDataPipeline:
    def __init__(self):
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.db = os.getenv("POSTGRES_DB")
        self.host = "localhost"
        self.port = os.getenv("POSTGRES_PORT", "5432")
        self.engine = create_engine(f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}")

    def fetch_ibge(self, url, column_name):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            data = response.json()
            serie = data[0]['resultados'][0]['series'][0]['serie']
            df = pd.DataFrame(list(serie.items()), columns=['mes_referencia', column_name])
            return df
        except Exception as e:
            print(f"Erro ao acessar IBGE ({column_name}): {e}")
            return pd.DataFrame()

    def run_pipeline(self):
        url_ipca = "https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/-24/variaveis/63?localidades=N1[all]"
        df_ipca = self.fetch_ibge(url_ipca, 'valor_ipca')

        url_varejo = "https://servicodados.ibge.gov.br/api/v3/agregados/8880/periodos/-24/variaveis/7169?localidades=N1[all]"
        df_varejo = self.fetch_ibge(url_varejo, 'indice_vendas_varejo')

        if df_ipca.empty or df_varejo.empty:
            print("Falha na extração.")
            return

        df_ipca['mes_referencia'] = df_ipca['mes_referencia'].astype(str).str.strip()
        df_varejo['mes_referencia'] = df_varejo['mes_referencia'].astype(str).str.strip()

        print(f"Cruzando {len(df_ipca)} linhas de IPCA com {len(df_varejo)} de Varejo...")
        
        df_final = pd.merge(df_ipca, df_varejo, on='mes_referencia', how='inner')
        
        print(f"Linhas após o cruzamento: {len(df_final)}")

        if len(df_final) == 0:
            print("⚠️ AVISO: O cruzamento resultou em 0 linhas. Verifique se os períodos coincidem.")
            # Imprime as datas das duas APIS para comparação de modelo
            print("Datas IPCA:", df_ipca['mes_referencia'].head(3).tolist())
            print("Datas Varejo:", df_varejo['mes_referencia'].head(3).tolist())
            return

        print("Limpando dados e preparando para o banco...")
        df_final['valor_ipca'] = pd.to_numeric(df_final['valor_ipca'], errors='coerce')
        df_final['indice_vendas_varejo'] = pd.to_numeric(df_final['indice_vendas_varejo'], errors='coerce')

        df_final = df_final.dropna(subset=['valor_ipca', 'indice_vendas_varejo'], how='all')

        if len(df_final) == 0:
            print("O DataFrame ficou vazio após a conversão numérica.")
            return

        print(f"Enviando {len(df_final)} linhas para o Postgres...")
        with self.engine.begin() as conn:
            df_final.to_sql('ext_analise_varejo_inflacao', conn, if_exists='replace', index=False)
        
        print(f"{len(df_final)} linhas carregadas no Postgres.")

if __name__ == "__main__":
    pipeline = GovDataPipeline()
    pipeline.run_pipeline()