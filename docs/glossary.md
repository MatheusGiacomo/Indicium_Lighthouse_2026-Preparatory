# 📖 Glossário Técnico

> "A clareza na terminologia é o primeiro passo para uma arquitetura de dados resiliente."

## 📝 Introdução

Este glossário funciona como um dicionário vivo de conceitos fundamentais explorados durante a fase de nivelamento para o **Indicium Lighthouse 2026**. Em projetos de consultoria, a precisão terminológica é vital para evitar ambiguidades entre equipes de engenharia e áreas de negócio. 

A estrutura abaixo consolida definições técnicas, siglas e conceitos da **Modern Data Stack (MDS)**, servindo como base para a documentação de futuros projetos e laboratórios práticos.

---

## 🏛️ Arquitetura e Armazenamento

* **OLTP (Online Transactional Processing):** Sistemas focados na execução de transações rápidas e operacionais (ex: bancos de dados de apps).
* **OLAP (Online Analytical Processing):** Sistemas otimizados para consultas complexas e análises históricas.
* **Data Warehouse (DW):** Repositório de dados estruturados e organizados para BI.
* **Data Lake:** Repositório que armazena dados em seu estado bruto (estruturados ou não).
* **Data Lakehouse:** Arquitetura que une a governança do DW com a flexibilidade e custo do Lake.
* **Cloud Data Warehouse:** Armazenamento analítico baseado em nuvem (ex: Snowflake, BigQuery) com separação de processamento e armazenamento.

## 🔄 Fluxo e Transformação de Dados

* **ETL (Extract, Transform, Load):** Fluxo tradicional onde a transformação ocorre antes da carga no destino.
* **ELT (Extract, Load, Transform):** Padrão da MDS onde o dado é carregado bruto e transformado dentro do Warehouse usando seu próprio poder de processamento.
* **Pipeline de Dados:** O conjunto de processos que movem os dados de um sistema para outro.
* **Idempotência:** Propriedade de um processo que permite que ele seja executado múltiplas vezes sem alterar o resultado final além da primeira execução (evita duplicidade).

## 📐 Modelagem Dimensional (Kimball)

* **Tabela Fato:** Tabela central que contém as métricas quantitativas de um evento de negócio.
* **Tabela Dimensão:** Tabela que contém os atributos descritivos que contextualizam os fatos.
* **Star Schema:** Modelo em que uma Fato é cercada por Dimensões, otimizando a leitura.
* **Granularidade (Grain):** O nível de detalhe de uma única linha em uma tabela.
* **SCD (Slowly Changing Dimension):** Técnicas para gerenciar mudanças nos atributos das dimensões ao longo do tempo.
* **Surrogate Key (SK):** Chave única gerada internamente no Data Warehouse, independente de chaves de sistemas externos.

## 🚀 Modern Data Stack

* **dbt (Data Build Tool):** Ferramenta que permite transformar dados dentro do Warehouse apenas com SQL e boas práticas de engenharia de software (versionamento, testes).
* **Orquestração:** O gerenciamento do fluxo de tarefas (DAGs), geralmente feito por ferramentas como o **Apache Airflow**.
* **Data Contracts:** Acordos entre produtores e consumidores de dados para garantir a qualidade e o formato na origem.
* **Data Observability:** Monitoramento contínuo da saúde dos dados (volume, frescor, distribuição e linhagem).
* **Linhagem de Dados (Lineage):** O rastro que o dado percorre desde a origem até o dashboard final.

---

## 🏗️ Infraestrutura e Banco de Dados (Lab 01)

### **Docker & Container**
Uma plataforma que permite empacotar uma aplicação e todas as suas dependências em um **container** isolado. Garante que o projeto rode da mesma forma em qualquer máquina ("Funciona na minha máquina e na sua").

### **PostgreSQL**
Sistema de Gerenciamento de Banco de Dados (SGBD) relacional de código aberto, utilizado como nosso *Data Warehouse* para armazenar os dados extraídos.

### **pgAdmin**
Interface gráfica (GUI) utilizada para gerenciar, visualizar e executar consultas SQL no banco de dados PostgreSQL de forma intuitiva.

### **Persistência de Dados (Volumes)**
Conceito que garante que os dados salvos dentro de um container Docker não sejam perdidos quando o container é parado ou deletado.

---

## 🐍 Programação e ETL (Lab 02)

### **API (Application Programming Interface)**
Um conjunto de definições e protocolos que permite que um software (nosso script Python) se comunique com outro (servidores do IBGE ou Banco Central) para solicitar dados.

### **JSON (JavaScript Object Notation)**
Formato leve de troca de dados, estruturado em chaves e valores, comumente retornado por APIs REST.

### **Pandas**
A principal biblioteca de Python para manipulação de dados. Utilizada para transformar arquivos JSON em **DataFrames** (tabelas em memória).

### **SQLAlchemy**
Uma biblioteca de mapeamento objeto-relacional (ORM) que permite ao Python se comunicar com o PostgreSQL de forma eficiente e segura.

---

## 🛡️ Conceitos de Engenharia e Qualidade

### **Atomicidade (Engine.begin)**
Princípio que garante que uma transação no banco de dados ocorra por completo ou não ocorra nada ("Tudo ou nada"). Evita que o banco receba apenas "metade" dos dados se o script falhar no meio do caminho.

### **Data Sanitization (Limpeza de Dados)**
O ato de identificar e tratar dados "sujos", como o caractere `..` retornado pelo IBGE, convertendo-os em formatos legíveis para o banco de dados (como `NULL` ou `NaN`).

### **Pivoting (Estratégia)**
Mudança de direção técnica durante o desenvolvimento. Exemplo: Alternar da API do Banco Central para a do IBGE quando a primeira apresenta instabilidade ou bloqueios.

### **User-Agent**
Um cabeçalho enviado nas requisições HTTP que identifica qual "cliente" está acessando o servidor. Essencial para evitar bloqueios de segurança (Erro 406) em servidores governamentais.

---

## 💡 Por que este Glossário é importante?

A estruturação deste documento, apoiada por pesquisas em fontes como **IBM, Databricks e AWS**, garante que o conhecimento adquirido no Módulo Zero da Indicium seja devidamente documentado.
