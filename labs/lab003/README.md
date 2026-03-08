# 🚀 Lighthouse Platform: Macroeconomic & Oil Intelligence E2E

A **Lighthouse Platform** é uma infraestrutura de dados de nível empresarial projetada para a extração, transformação, auditoria e visualização de indicadores macroeconômicos globais. O sistema utiliza uma *Modern Data Stack* para correlacionar dados do PIB e preços do Petróleo, garantindo integridade via testes automatizados e governança através de logs de auditoria persistentes.

---

## 🏗️ Arquitetura do Sistema (Medallion Architecture)

O projeto segue os princípios da arquitetura de medalhão para garantir a qualidade progressiva dos ativos de dados:

* **Ingestion Layer (Raw):** Scripts Python automatizados que extraem dados brutos das APIs do Banco Mundial e Yahoo Finance, persistindo-os no PostgreSQL.
* **Silver Layer (Cleansing):** O **dbt** realiza a limpeza, normalização e tipagem, transformando dados brutos em tabelas relacionais confiáveis.
* **Gold Layer (Analytics):** Modelos dimensionais otimizados para consumo, onde reside a lógica de negócio e a unificação dos indicadores.
* **Audit Layer (Security):** Camada transversal que monitora proativamente a integridade da camada Gold.

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Motivação Técnica |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.13 | Processamento eficiente e integração com APIs financeiras. |
| **Data Warehouse** | PostgreSQL 15 | Robustez relacional e suporte avançado a triggers de auditoria. |
| **Containerização** | Docker | Isolamento de dependências e paridade entre ambientes. |
| **Transformação** | dbt (Data Build Tool) | Modelagem SQL versionada com foco em linhagem e testes. |
| **Orquestração** | Prefect 3.0 | Gestão de workflows com observabilidade e retentativas automáticas. |
| **Dashboard** | Streamlit | Entrega ágil de visualizações analíticas de alto impacto. |

---

## 🔐 Segurança, Governança e dbt Hooks

Um diferencial crítico deste sistema é a sua camada de Segurança de Dados. Implementei uma política de auditoria rigorosa para proteger a camada Gold:

1.  **Auditoria via Triggers:** Criei um schema isolado (`audit`) com gatilhos SQL que registram qualquer tentativa de `UPDATE` ou `DELETE` manual.
2.  **Idempotência com dbt Hooks:** Como o dbt recria tabelas em cada execução, utilizei `post-hooks` no arquivo `dbt_project.yml`. Isso garante que, toda vez que uma tabela for reconstruída, o "vigia" (trigger) seja reinstalado automaticamente, eliminando brechas de segurança.
3.  **Controle de Acesso (RBAC):** Segregação de usuários entre o proprietário do processo de ETL (`user_dbt`) e o usuário final do dashboard (`user_dashboard`), limitando privilégios ao estritamente necessário.

---

## ⚙️ Configuração e Instalação

### Pré-requisitos
* Docker & Docker Compose
* Python 3.12+
* Ambiente Virtual Python (`.venv`)

### Execução Passo a Passo

1. **Subir Banco de Dados:**
   ```bash
   docker-compose up -d

2. **Configurar ambiente:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # No Windows: .venv\Scripts\activate
   pip install -r requirements.txt

3. **Executar a Orquestração:**
   ```bash
   python orchestrator.py
  O Prefect iniciará automaticamente a ingestão, as transformações dbt e os testes de qualidade.

4. **Lançar Dashboard:**
   ```bash
   streamlit run app.py

## 🚀 Troubleshooting e Resiliência (Post-Mortem)

O desenvolvimento deste sistema passou por um processo extenso de depuração, resultando em uma plataforma mais resiliente:

* **Gestão de Ambiente Virtual:** Superei conflitos de ambiente configurando o orquestrador para localizar dinamicamente o executável do Python dentro do `.venv`, evitando falhas de `ModuleNotFound` em tarefas automatizadas.
* **Estabilidade do dbt em Subprocessos:** Ajustei a chamada do dbt para utilizar o `dbt.exe` diretamente da pasta de scripts do ambiente virtual, resolvendo problemas de execução do módulo `__main__`.
* **Persistência de Dados:** Implementei volumes Docker para garantir que, mesmo após o reinício dos containers, o histórico de logs de auditoria e as permissões de banco não sejam perdidos.
* **Tratamento de Saída (Encoding):** Blindei o orquestrador contra erros de caracteres especiais (Unicode) em sistemas Windows, utilizando captura de logs com tratamento de erro via substituição, garantindo que o fluxo não seja interrompido por emojis ou símbolos de bibliotecas externas.

---

## 📊 Visualização e Qualidade

O dashboard final só exibe dados que passaram com **100% de sucesso nos dbt tests** (*uniqueness*, *not_null* e *referential integrity*). Isso garante que o usuário final nunca tome decisões baseadas em dados corrompidos ou incompletos.

---

## 🎯 Conclusão

A **Lighthouse Platform** estabelece uma base sólida para inteligência de dados no setor de energia e macroeconomia. Ao unir a flexibilidade do Python com a governança rigorosa do dbt e a orquestração moderna do Prefect, entrego não apenas dados, mas confiança analítica.

---

## 🖼️ Visualização do Ecossistema

Abaixo, apresento as principais interfaces que compõem a operação da **Lighthouse Platform**:

### 1. Dashboard Analítico (Streamlit)
Interface final de consumo, onde os dados do PIB e Petróleo são correlacionados. Exibe gráficos de tendências, variações percentuais e indicadores de saúde macroeconômica.

![Dashboard do Streamlit](/docs/images/streamlit.png)

### 2. Orquestração e Observabilidade (Prefect)
Painel de controle do fluxo de dados (Pipeline E2E). Aqui é possível monitorar o status de cada *task*, verificar logs de execução em tempo real e gerenciar retentativas automáticas em caso de falha nas APIs.

![Dashboard do Prefect](/docs/images/prefect.png)

### 3. Gestão e Auditoria de Dados (pgAdmin)
Visão técnica da camada de persistência no PostgreSQL. Demonstra a estrutura das tabelas nas camadas *Silver* e *Gold*, além do schema de auditoria que registra a integridade dos dados.

![Interface pgAdmin](/docs/images/pgadmin.png)

---

### 👤 Autor
Matheus Di Giacomo
Desenvolvido com foco em engenharia de dados robusta e segurança. 
> *“In God we trust; all others must bring data.”* – W. Edwards Deming
