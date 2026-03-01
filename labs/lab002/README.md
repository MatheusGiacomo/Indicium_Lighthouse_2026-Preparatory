# Lab 02: Engenharia de Dados com Python & SQL 🚀

## 📋 Introdução
Este repositório documenta o desenvolvimento do segundo laboratório prático da trilha **Lighthouse 2026**. O foco desta semana foi a transição da infraestrutura estática (Lab 01) para a criação de **pipelines de dados dinâmicos**, utilizando Python para extrair dados de APIs governamentais e integrá-los de forma resiliente em um banco de dados PostgreSQL. Para usar os scripts do lab 02, é importante que você já tenha a pasta do lab 01 em seu computador.



---

## 🏗️ Arquitetura do Pipeline
O fluxo de dados foi projetado seguindo princípios de modularidade e Programação Orientada a Objetos (POO):
1.  **Extração:** Consumo de APIs REST (IBGE/SIDRA).
2.  **Transformação:** Limpeza de caracteres especiais, normalização de tipos e cruzamento (*Merge*) de fontes distintas via Pandas.
3.  **Carga:** Persistência em banco de dados PostgreSQL (Docker) utilizando SQLAlchemy com garantia de atomicidade.

---

## 🛠️ Tecnologias Utilizadas
* **Python 3.13:** Linguagem core para a lógica de ETL.
* **Pandas:** Biblioteca para manipulação e tratamento de estruturas de dados tabulares.
* **SQLAlchemy:** Interface de conexão e toolkit SQL para comunicação com o banco.
* **PostgreSQL 15:** Banco de dados relacional para armazenamento dos dados.
* **Docker & Docker Compose:** Orquestração do ambiente de banco de dados.

---

## 🚧 Desafios Enfrentados & Soluções (Troubleshooting)

Um Engenheiro de Dados é, acima de tudo, um resolvedor de problemas. Abaixo, listo os obstáculos técnicos superados durante este Lab:

### 1. Bloqueio de Segurança em APIs (HTTP Error 406)
**Problema:** Ao tentar acessar a API do Banco Central (BCB), o servidor retornava erro `406 Not Acceptable`, bloqueando a biblioteca `requests`.
**Solução:** Implementação de **Custom Headers** simulando um `User-Agent` de navegador real. Diante da instabilidade persistente, realizei o **Pivoting de Fonte** para o IBGE, garantindo o cumprimento do cronograma.

### 2. Sujeira nos Dados (Caracteres Especiais)
**Problema:** A API do IBGE utiliza o símbolo `..` para representar dados nulos ou não processados, causando falha crítica (`ValueError`) na conversão numérica.
**Solução:** Utilização do método `pd.to_numeric(errors='coerce')`. 
**Impacto:** Esta escolha técnica transforma caracteres inválidos em `NaN`, permitindo que o pipeline prossiga sem interrupções.

### 3. Perda de Dados na Limpeza (*Dropna* vs. Preservação)
**Problema:** O uso inicial de `.dropna()` resultava em 0 linhas enviadas ao banco, pois os meses recentes de 2024 ainda continham nulos parciais.
**Solução:** Substituição da exclusão pela preservação de **Valores Nulos (NULLs)**, mantendo a integridade da série histórica.

---

## 📊 SQL Avançado & Análise de Dados

Após a carga, os dados foram validados utilizando **Window Functions** para gerar insights macroeconômicos.

## 📑 Lições Aprendidas

A execução deste laboratório proporcionou aprendizados fundamentais sobre o ciclo de vida do dado e robustez de pipelines:

* **Idempotência:** Configuração do pipeline para execuções múltiplas sem duplicação de registros (estratégia de `replace`), garantindo a consistência do estado final do banco de dados.
* **Resiliência e Falha Segura:** Implementação de tratamentos de exceção e logs claros para mitigar falhas de rede e instabilidades em APIs externas, evitando interrupções silenciosas.
* **Atomicidade em Transações:** Uso do método `engine.begin()` via **SQLAlchemy** para garantir o princípio *Tudo ou Nada*. Os dados só são persistidos se a transação for concluída integralmente, prevenindo corrupção de tabelas.
* **Qualidade do Dado (Data Quality):** Tratamento semântico de fontes (ex: saneamento de caracteres especiais como `..` do IBGE). A engenharia de dados aqui atua na limpeza ativa para garantir a integridade da análise posterior.

---

## 🚀 Próximos Passos (Roadmap)

O projeto seguirá um cronograma de evolução técnica focado em escalabilidade e governança:

1.  **Camada de Transformação (dbt):** Migrar a lógica de negócio da *Landing Zone* para tabelas modeladas (*Trusted/Analytics*) utilizando SQL modular com **Data Build Tool**.
2.  **Orquestração de Fluxos:** Implementar ferramentas de agendamento como **Apache Airflow** ou **Prefect** para automatizar a execução dos scripts Python.
3.  **Data Quality Tests:** Automatizar a validação de intervalos lógicos (ex: inflação e índices de varejo) utilizando **Great Expectations** ou testes nativos do dbt.
4.  **Data Visualization:** Conectar o Data Warehouse a uma ferramenta de BI (**Metabase** ou **Power BI**) para monitoramento de correlações macroeconômicas.

---