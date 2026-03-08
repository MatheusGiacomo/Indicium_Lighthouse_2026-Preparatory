import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_data():
    engine = create_engine("postgresql://user_dashboard:dash_pass_789@localhost:5433/dw_lighthouse")
    return pd.read_sql("SELECT * FROM gold.fct_analise_macro ORDER BY reference_year ASC", engine)

st.set_page_config(page_title="Lighthouse Data Platform", layout="wide")

st.title("📊 Dashboard de Análise Macroeconômica")
st.markdown("Visualização da Camada **Gold** — PIB vs Petróleo")

try:
    df = get_data()

    if not df.empty:
        # Sidebar com filtro de ID do País
        st.sidebar.header("Filtros")
        paises = st.sidebar.multiselect("Selecione os IDs dos Países", df['country_id'].unique(), default=df['country_id'].unique())
        
        df_filtered = df[df['country_id'].isin(paises)]

        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Evolução do PIB (USD)")
            # Gráfico de linhas por país
            chart_pib = df_filtered.pivot(index='reference_year', columns='country_id', values='gdp_usd')
            st.line_chart(chart_pib)
            
        with c2:
            st.subheader("Média do Petróleo (Brent)")
            # Média anual única do petróleo
            df_oil = df_filtered.groupby('reference_year')['media_petroleo'].mean()
            st.line_chart(df_oil)

        st.subheader("Tabela de Dados Consolidados")
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.warning("Aguardando dados da camada Gold. Certifique-se de rodar o dbt.")

except Exception as e:
    st.error(f"Erro ao carregar o dashboard: {e}")