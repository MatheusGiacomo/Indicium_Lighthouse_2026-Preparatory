-- Criação de Schemas (Incluindo o de Auditoria)
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS audit;

-- Definição de Proprietários
ALTER SCHEMA silver OWNER TO user_dbt;
ALTER SCHEMA gold OWNER TO user_dbt;
ALTER SCHEMA audit OWNER TO user_dbt;

-- Permissões Granulares: Ingestão (Python)
GRANT USAGE, CREATE ON SCHEMA raw TO user_ingestion;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA raw TO user_ingestion;
ALTER DEFAULT PRIVILEGES IN SCHEMA raw GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO user_ingestion;

-- Permissões Granulares: Transformação (dbt)
GRANT USAGE ON SCHEMA raw TO user_dbt;
GRANT SELECT ON ALL TABLES IN SCHEMA raw TO user_dbt;
GRANT ALL PRIVILEGES ON SCHEMA silver TO user_dbt;
GRANT ALL PRIVILEGES ON SCHEMA gold TO user_dbt;
GRANT ALL PRIVILEGES ON SCHEMA audit TO user_dbt; -- Acesso para dbt Hooks

ALTER DEFAULT PRIVILEGES IN SCHEMA silver GRANT ALL ON TABLES TO user_dbt;
ALTER DEFAULT PRIVILEGES IN SCHEMA gold GRANT ALL ON TABLES TO user_dbt;
ALTER DEFAULT PRIVILEGES FOR USER user_ingestion IN SCHEMA raw GRANT SELECT ON TABLES TO user_dbt;

-- Permissões Granulares: Dashboard (Streamlit)
GRANT USAGE ON SCHEMA gold TO user_dashboard;
ALTER DEFAULT PRIVILEGES FOR USER user_dbt IN SCHEMA gold GRANT SELECT ON TABLES TO user_dashboard;
GRANT SELECT ON ALL TABLES IN SCHEMA gold TO user_dashboard;

-- Estrutura Inicial de Auditoria
CREATE TABLE IF NOT EXISTS audit.logs (
    id SERIAL PRIMARY KEY,
    usuario TEXT DEFAULT current_user,
    tabela TEXT,
    operacao TEXT,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
GRANT SELECT, INSERT ON audit.logs TO user_dbt;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA audit TO user_dbt;