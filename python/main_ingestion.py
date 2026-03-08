import os
import yfinance as yf
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EnterpriseIngestor:
    def __init__(self):
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.db = os.getenv("POSTGRES_DB")
        self.host = "localhost"
        self.port = "5433"
        
        self.engine = create_engine(f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}")

    def add_audit_metadata(self, df):
        """Adiciona colunas de auditoria aos DataFrames"""
        df['ingestion_timestamp'] = datetime.now()
        df['source_system'] = 'Enterprise_Pipeline_v1'
        return df

    def ingest_market_data(self, tickers=["USO", "GC=F", "^BVSP"]):
        """Extrai dados de commodities e índices do Yahoo Finance"""
        print(f"Extraindo dados históricos (2014-2024): {tickers}")
        
        data = yf.download(tickers, start="2014-01-01", end="2024-12-31", interval="1d")
        df = data['Close'].reset_index()
    
        # Limpeza e padronização de nomes de colunas
        df.columns = [col.replace('^', '').replace('=F', '').lower() for col in df.columns]
        df = df.rename(columns={'date': 'reference_date'})
    
        # Renomeia 'uso' para 'cl' para manter compatibilidade com o SQL do dbt
        if 'uso' in df.columns:
            df = df.rename(columns={'uso': 'cl'})

        print(f"Check de Datas: {df['reference_date'].min()} até {df['reference_date'].max()}")
    
        df = self.add_audit_metadata(df)
        df.to_sql('market_commodities', self.engine, schema='raw', if_exists='replace', index=False)
        print("Dados de mercado carregados em raw.market_commodities")

    def ingest_world_bank_data(self):
        """Extrai Indicadores de Desenvolvimento (PIB per capita) do World Bank"""
        print("Extraindo dados do Banco Mundial (World Bank)...")
        countries = "br;us;cn"
        indicator = "NY.GDP.PCAP.CD"
        url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}?format=json&per_page=100&date=2014:2024"
        
        response = requests.get(url)
        json_data = response.json()
        
        # O índice 1 contém a lista de dados da API
        raw_list = json_data[1]
        
        flat_data = [
            {
                "country_id": item['countryiso3code'],
                "year": item['date'],
                "gdp_per_capita": item['value']
            } for item in raw_list if item['value'] is not None
        ]
        
        df = pd.DataFrame(flat_data)
        df = self.add_audit_metadata(df)
        df.to_sql('world_bank_gdp', self.engine, schema='raw', if_exists='replace', index=False)
        print(f"Dados do Banco Mundial ({len(df)} registros) carregados em raw.world_bank_gdp")

    def ingest_reference_iso_codes(self):
        """Carrega dados de referência estáticos para mapeamento de países"""
        print("Carregando metadados de referência (Países ISO)...")
        iso_data = [
            {"iso_code": "BRA", "region": "South America", "currency": "BRL"},
            {"iso_code": "USA", "region": "North America", "currency": "USD"},
            {"iso_code": "CHN", "region": "East Asia", "currency": "CNY"}
        ]
        df = pd.DataFrame(iso_data)
        df = self.add_audit_metadata(df)
        df.to_sql('iso_country_mapping', self.engine, schema='raw', if_exists='replace', index=False)
        print("Metadados carregados em raw.iso_country_mapping")

    def apply_privileges(self):
        """Cria schemas, funções de auditoria e garante permissões"""
        dbt_user = os.getenv("DBT_USER")
        
        print("Preparando ambiente do banco (Schemas e Funções)...")
        with self.engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS audit;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold;"))
            
            # Esta é uma função dummy que apenas retorna nulo, 
            # permitindo que o dbt continue sem quebrar.
            conn.execute(text("""
                CREATE OR REPLACE FUNCTION audit.process_audit()
                RETURNS trigger AS $$
                BEGIN
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """))
            
            if dbt_user and dbt_user != self.user:
                print(f"Aplicando permissões para: {dbt_user}...")
                queries = [
                    f"GRANT USAGE ON SCHEMA raw TO {dbt_user};",
                    f"GRANT USAGE ON SCHEMA audit TO {dbt_user};",
                    f"GRANT ALL ON SCHEMA audit TO {dbt_user};",
                    f"GRANT ALL ON SCHEMA silver TO {dbt_user};",
                    f"GRANT ALL ON SCHEMA gold TO {dbt_user};",
                    f"GRANT SELECT ON ALL TABLES IN SCHEMA raw TO {dbt_user};",
                    f"ALTER DEFAULT PRIVILEGES IN SCHEMA raw GRANT SELECT ON TABLES TO {dbt_user};"
                ]
                for query in queries:
                    conn.execute(text(query))
            
            conn.commit()
        print("Ambiente e permissões configurados com sucesso!")

    def run_pipeline(self):
        """Executa o fluxo completo de ingestão e permissões"""
        self.ingest_market_data()
        self.ingest_world_bank_data()
        self.ingest_reference_iso_codes()
        
        self.apply_privileges()
        
        print("\n Pipeline RAW finalizado. Dados e permissões prontos para o dbt!")

if __name__ == "__main__":
    ingestor = EnterpriseIngestor()
    ingestor.run_pipeline()