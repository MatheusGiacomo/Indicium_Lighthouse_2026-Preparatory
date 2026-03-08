# 🐍 Python Data Ingestion Layer

Esta pasta contém o script responsável pela primeira etapa do pipeline: a **Extração e Carga (E&L)**.

## 📋 O que este componente faz:
* **Consumo de APIs:** Scripts que se conectam à API do World Bank (PIB) e Yahoo Finance (Petróleo).
* **Tratamento de Dados:** Utiliza **Pandas** para limpeza inicial, padronização de tipos e tratamento de datas.
* **Persistência:** Carregamento idempotente no PostgreSQL via **SQLAlchemy**.

## 🛠️ Principais Bibliotecas:
* `requests`: Comunicação com APIs REST.
* `pandas`: Manipulação e estruturação de dados.
* `sqlalchemy`: Interface robusta com o banco de dados.
* `python-dotenv`: Gestão segura de credenciais.

> **Nota:** Estes scripts são orquestrados pelo Prefect no diretório principal.
