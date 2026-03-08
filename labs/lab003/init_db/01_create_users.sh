#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- 1. Criar Usuários apenas se não existirem (usando as variáveis do .env)
    DO \$\$ 
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$INGEST_USER') THEN
            CREATE USER $INGEST_USER WITH PASSWORD '$INGEST_PASSWORD';
        END IF;
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$DBT_USER') THEN
            CREATE USER $DBT_USER WITH PASSWORD '$DBT_PASSWORD';
        END IF;
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$DASH_USER') THEN
            CREATE USER $DASH_USER WITH PASSWORD '$DASH_PASSWORD';
        END IF;
    END \$\$;

    -- 2. Permissões de Conexão Base
    GRANT CONNECT ON DATABASE $POSTGRES_DB TO $INGEST_USER, $DBT_USER, $DASH_USER;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $DBT_USER;
EOSQL