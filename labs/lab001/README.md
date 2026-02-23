# 🧪 Lab 001: Infraestrutura Modern Data Stack com Docker

> "Ambientes reprodutíveis são a base de uma engenharia de dados confiável."

## 🎯 Objetivo
Configurar um ambiente de desenvolvimento local utilizando **Docker** para simular um ecossistema de dados moderno, integrando um banco de dados transacional/analítico (**PostgreSQL**) e uma interface de gerenciamento (**pgAdmin**).

---

## 🛠️ Tecnologias Utilizadas
* **Docker & Docker Compose:** Orquestração de containers.
* **PostgreSQL 18:** Banco de dados relacional.
* **pgAdmin 4:** Ferramenta de administração e Query Tool.
* **SQL:** Linguagem para DDL (Data Definition) e DML (Data Manipulation).

---

## 🚀 Como Executar o Ambiente

### 1. Preparação das Credenciais
Na pasta `/docker`, você encontrará o arquivo `.env.example`. 
1. Crie uma cópia deste arquivo e renomeie para `.env`.
2. Preencha as variáveis de ambiente com suas credenciais preferidas.

### 2. Subindo os Containers
No terminal, dentro da pasta `/docker`, execute:
docker-compose up -d

### 📐 Modelagem de Dados (Star Schema)

A modelagem dimensional aplicada neste laboratório segue a **Metodologia Kimball**, focada na facilidade de consulta e performance analítica. Estruturamos os dados em um **Star Schema (Esquema Estrela)** para separar as métricas de negócio do seu contexto descritivo.

### Entidades do Modelo:

1.  **Tabela Fato (`fato_vendas`):** * **O que é:** O centro do modelo, onde registramos os eventos de venda.
    * **Métricas:** `quantidade` e `valor_total` (medidas aditivas).
    * **Grão:** Uma linha por item vendido em cada transação.

2.  **Tabelas Dimensão (Contexto):**
    * **`dim_clientes`:** Informações geográficas e de segmento dos compradores.
    * **`dim_produtos`:** Catálogo de produtos com categorias e preços base.
    * **`dim_tempo`:** Dimensão essencial para análises de séries temporais (ano, mês, dia da semana, trimestre).



> **OBS:** O uso de chaves estrangeiras (`REFERENCES`) na tabela fato garante a **integridade referencial**, impedindo que uma venda seja registrada para um produto ou cliente inexistente no sistema.

---

## 🧠 Aprendizados e Troubleshooting

O desenvolvimento deste ambiente trouxe alguns desafios técnicos:

### 1. Persistência e Volumes (Postgres 18)
* **Desafio:** O container do Postgres entrava em loop de reinicialização devido a uma mudança de padrão nas imagens Docker recentes.
* **Solução:** Ajuste do ponto de montagem do volume de `/var/lib/postgresql/data` para `/var/lib/postgresql`. Isso permitiu que o Postgres gerenciasse sua estrutura de diretórios interna de forma compatível com as versões 18.

### 2. Networking entre Containers
* **Desafio:** Dificuldade inicial em conectar o **pgAdmin** ao **Postgres** usando `localhost`.
* **Aprendizado:** Em redes Docker (Bridge), o termo `localhost` refere-se ao próprio container. Para a comunicação *inter-container*, aprendi a utilizar o **Service Name** (`db`) definido no `docker-compose.yml`, que o Docker resolve automaticamente via DNS interno.

### 3. Segurança e Variáveis de Ambiente (`.env`)
* **Desafio:** Evitar o vazamento de credenciais sensíveis no controle de versão.
* **Solução:** Implementação de um fluxo profissional usando um arquivo `.env` para armazenamento de segredos e um `.env.example` para documentação. O arquivo `.env` foi devidamente ignorado no `.gitignore`, seguindo as melhores práticas de **DevSecOps**.

### 4. Idempotência no Seed

* **Aprendizado:** O script `seed.sql` foi desenhado com comandos `DROP TABLE IF EXISTS`. Isso garante que o script possa ser rodado múltiplas vezes sem erros, mantendo o ambiente sempre em um estado conhecido e limpo (idempotência).
