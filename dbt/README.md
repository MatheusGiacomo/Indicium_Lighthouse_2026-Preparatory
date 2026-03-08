# 🛠️ dbt Transformation Layer (Analytics Engineering)

Aqui reside a inteligência de negócio do projeto. Utilizei o **dbt (Data Build Tool)** para transformar dados brutos em ativos de dados prontos para análise.

## 🏗️ Estrutura de Modelagem:
* **Models/Silver:** Limpeza profunda, renomeação de colunas para padrão snake_case e cast de tipos.
* **Models/Gold:** Tabelas fatos e dimensionais (ex: `fct_analise_macro`) que unem os indicadores de economia e energia.

## 🛡️ Qualidade e Governança:
* **Data Testing:** Testes de unicidade, integridade referencial e valores não nulos aplicados em cada execução.
* **Documentation:** Linhagem de dados automatizada (Lineage Graph) para rastreabilidade total.
* **Persistence:** Uso de *table* e *incremental* materializations para otimizar performance.

## 🚀 Comandos Úteis:
* `dbt run`: Executa as transformações.
* `dbt test`: Valida a qualidade dos dados.
