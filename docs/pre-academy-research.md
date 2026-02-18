# 🔍 Pesquisa de Fundamentos e Modern Data Stack

> "A excelência não é um ato, mas um hábito de preparação contínua."

## 📖 Introdução e Justificativa

Este documento é o resultado de uma imersão técnica realizada de forma antecipada, utilizando como bússola as diretrizes apresentadas no **Módulo Zero** do programa Lighthouse. 

Diferente de uma pesquisa genérica, este levantamento foi estruturado a partir dos **Guias de Estudo oficiais** (Analytics Engineering, Data Engineering, Data Science e IA) e das sessões de **Data Talks** disponibilizadas pela Indicium. A decisão de consolidar estes conceitos antes do início das aulas práticas fundamenta-se em três pilares estratégicos:

### 🎯 Por que iniciar esta pesquisa a partir do Módulo Zero?

1.  **Alinhamento com a Metodologia Indicium:** O Módulo Zero deixou claro que a transição para carreiras de dados exige uma mudança de mindset. Esta pesquisa visa sedimentar o "pensamento de Analytics Engineer" e a compreensão da Modern Data Stack (MDS) antes da execução técnica.
2.  **Otimização do Ciclo de Aprendizado:** Ao estudar previamente os temas sugeridos nos guias de Engenharia e Analytics, garanto que o tempo das aulas ao vivo será utilizado para discussões de alto nível e resolução de problemas complexos, maximizando o aproveitamento da mentoria.
3.  **Resposta à Proatividade Exigida:** As trilhas de carreira e os talks sobre "como aprender tecnologia de forma eficiente" enfatizaram que a autonomia é um diferencial no Lighthouse. Este documento é a aplicação prática dessa orientação: transformar as referências teóricas do Módulo Zero em conhecimento estruturado.
4.  **Visão Holística (Full Stack Data):** Inspirado pela variedade de guias (Data Analytics a IA), busquei entender como essas áreas se conectam dentro da arquitetura que a Indicium implementa, garantindo uma visão sistêmica do pipeline de dados.

---

## 🛠️ Eixos de Estudo (Diretrizes do Módulo 0)

Com base nos referenciais técnicos apresentados nos guias de estudo, esta pesquisa foca em:

* **Fundamentos Analíticos:** Diferenciação entre ambientes transacionais (OLTP) e analíticos (OLAP).
* **Modelagem de Dados:** O pilar da Analytics Engineering conforme sugerido na "Aula Zero".
* **Arquitetura de Nuvem:** O papel dos Cloud Data Warehouses na escalabilidade de projetos.
* **Ferramental Estratégico:** Introdução conceitual ao dbt e práticas de versionamento.

---

## 🗄️ Arquiteturas de Processamento: OLTP vs. OLAP

Para dominar a Engenharia de Dados, é fundamental entender onde os dados nascem e para onde eles vão. Abaixo, detalho as duas arquiteturas principais com base nas definições técnicas da IBM.

### 1. OLTP (Online Transactional Processing)
O foco aqui é a **execução**. São sistemas voltados para transações rápidas e frequentes.

* **Funcionamento:** Processa grandes volumes de transações simples (INSERT, UPDATE, DELETE) de forma simultânea.
* **Características Principais:**
    * **Alta Disponibilidade:** Precisa estar no ar 24/7 (ex: sistema de um banco).
    * **Velocidade:** Respostas em milissegundos.
    * **Normalização:** Dados são organizados para evitar redundância (geralmente em várias tabelas relacionadas).
    * **Propriedades ACID:** Garante que as transações sejam Atômicas, Consistentes, Isoladas e Duráveis.
* **Exemplos Práticos:**
    * Sistemas de PDV (caixa de supermercado).
    * Aplicativos de Internet Banking.
    * Sistemas de reserva de passagens aéreas.

### 2. OLAP (Online Analytical Processing)
O foco aqui é a **análise**. São sistemas voltados para consultas complexas e grandes volumes históricos.

* **Funcionamento:** Consolida dados de diversas fontes OLTP para permitir descobertas, relatórios e BI.
* **Características Principais:**
    * **Multidimensionalidade:** Permite analisar dados sob diferentes perspectivas (Tempo, Geografia, Produto).
    * **Dados Históricos:** Armazena dados de meses ou anos para identificar tendências.
    * **Consultas Complexas:** Frequentemente envolve agregações (`SUM`, `AVG`, `COUNT`) em milhões de linhas.
    * **Desnormalização:** Dados são organizados para performance de leitura (ex: Star Schema).
* **Exemplos Práticos:**
    * Relatórios de vendas anuais comparativos.
    * Previsão de demanda de estoque.
    * Análise de comportamento do consumidor (Churn).

---

### 📊 Tabela Comparativa

| Característica | OLTP (Transacional) | OLAP (Analítico) |
| :--- | :--- | :--- |
| **Objetivo** | Executar o negócio (Operacional) | Analisar o negócio (Estratégico) |
| **Fonte de Dados** | Operações em tempo real | Dados consolidados de OLTPs |
| **Queries** | Simples e rápidas | Complexas e demoradas |
| **Volume de Dados** | Gigabytes (dados atuais) | Terabytes/Petabytes (histórico) |
| **Usuários** | Clientes, atendentes, sistemas | Analistas, Cientistas de Dados, Diretores |

---

### 💡 Modern Data Stack
Na consultoria, o Engenheiro de Dados utiliza processos de **ELT** para extrair dados de sistemas **OLTP** (Postgres, MySQL, APIs) e carregá-los em um ambiente **OLAP** (Snowflake, BigQuery). Uma vez no ambiente OLAP, usamos o **dbt** para transformar esses dados brutos em modelos dimensionais que facilitam a vida do analista de BI.

---

### 🧊 O Conceito de Cubo OLAP
Diferente de uma tabela 2D (linhas e colunas), um **Cubo OLAP** é uma estrutura multidimensional que permite visualizar dados através de várias "dimensões".

* **Funcionamento:** Imagine um cubo onde uma face é o **Tempo** (anos/meses), outra é o **Produto** e a outra é a **Região**. O valor dentro do cubo (a **Métrica**) seria o total de vendas.
* **Operações Principais:**
    * **Drill-down:** Aumentar o detalhe (ex: de Ano para Meses).
    * **Roll-up:** Consolidar os dados (ex: de Cidades para Estados).
    * **Slice & Dice:** Filtrar e "fatiar" o cubo para ver apenas uma parte específica.

---

### 🚀 Variações de Arquitetura OLAP

Dependendo de como os dados são armazenados e processados, o OLAP se divide em três modelos principais:

#### 1. MOLAP (Multidimensional OLAP)
Os dados são armazenados em cubos proprietários, altamente indexados e pré-calculados.
* **Uso:** Quando a performance de leitura é crítica e as consultas são repetitivas.
* **Prós:** Velocidade absurda em grandes volumes.
* **Contras:** Menos flexível; se você precisar de uma análise que não foi pré-calculada, o sistema sofre.

#### 2. ROLAP (Relational OLAP)
Os dados permanecem em bancos de dados relacionais tradicionais. A "lógica do cubo" é aplicada via SQL complexo em tempo de execução.
* **Uso:** Quando os dados mudam com frequência ou a flexibilidade de consulta é prioridade.
* **Prós:** Escalável e utiliza a infraestrutura SQL já existente.
* **Contras:** Pode ser mais lento que o MOLAP para agregações massivas, pois processa tudo na hora.

#### 3. HOLAP (Hybrid OLAP)
O "melhor dos dois mundos". Mantém os dados detalhados no banco relacional (ROLAP) e as agregações pré-calculadas em cubos (MOLAP).
* **Uso:** Grandes corporações que precisam de detalhe máximo e velocidade em relatórios executivos.

---

### ☁️ OLAP na Nuvem

Antigamente, manter sistemas OLAP exigia servidores gigantescos e caros. Hoje, a **Modern Data Stack** mudou o jogo com o **Cloud OLAP**.

* **Arquitetura Desacoplada:** Ferramentas como **Snowflake** e **BigQuery** separam o Armazenamento (Storage) do Processamento (Compute). Você paga apenas pelo que usa.
* **Elasticidade:** Se você precisa rodar uma query em 1 bilhão de linhas às 9h da manhã, a nuvem escala 100 servidores para você e depois os desliga.
* **Diferencial técnico:** No Cloud OLAP moderno, a distinção entre ROLAP e MOLAP ficou tênue, pois o processamento em nuvem é tão rápido que muitas vezes não precisamos mais "pré-calcular" cubos rígidos.

![Arquitetura OLAP e OLTP](images/OLAP-OLTP.png)

---

## 🔄 Integração de Dados: ETL vs. ELT

A integração de dados é o processo de combinar dados de múltiplas fontes em um repositório centralizado. A principal diferença entre ETL e ELT reside na ordem em que os dados são transformados e onde esse processamento ocorre.

### 1. ETL (Extract, Transform, Load)
No modelo tradicional, os dados são transformados em um servidor secundário (staging area) antes de serem carregados no destino final.

* **Funcionamento:** Os dados são extraídos das fontes, passam por um processo de limpeza e formatação fora do banco de dados de destino e, somente após estarem "prontos", são carregados no Data Warehouse.
* **Características Principais:**
    * **Processamento Externo:** Depende de motores de processamento dedicados para a transformação.
    * **Conformidade e Privacidade:** Ideal para remover dados sensíveis (LGPD/GDPR) antes mesmo de chegarem ao armazenamento.
    * **Estrutura Rígida:** Requer que o esquema de destino seja definido antes da carga (Schema-on-write).
* **Uso Ideal:** Ambientes com dados altamente estruturados e limitações de processamento no banco de dados de destino (Sistemas On-premise).

### 2. ELT (Extract, Load, Transform)
O modelo moderno, impulsionado pela computação em nuvem, onde o dado bruto é carregado diretamente e a transformação utiliza o poder do destino.

* **Funcionamento:** Os dados são extraídos e carregados imediatamente no Data Warehouse ou Data Lake. A transformação ocorre internamente, utilizando SQL ou linguagens de processamento distribuído.
* **Características Principais:**
    * **Alta Escalabilidade:** Utiliza a elasticidade de Cloud Data Warehouses (como Snowflake e BigQuery).
    * **Flexibilidade:** Permite carregar dados brutos sem uma estrutura pré-definida (Schema-on-read), facilitando análises futuras.
    * **Velocidade de Ingestão:** O processo de carga é muito mais rápido, pois não há o gargalo da transformação prévia.
* **Uso Ideal:** Big Data, Modern Data Stack e projetos que exigem agilidade na disponibilização de novos dados.

---

### 📊 Tabela Comparativa

| Característica | ETL (Tradicional) | ELT (Moderno) |
| :--- | :--- | :--- |
| **Sequência** | Extrair → Transformar → Carregar | Extrair → Carregar → Transformar |
| **Local de Transformação** | Servidor de Processamento Independente | No próprio Data Warehouse/Lake |
| **Tempo de Carga** | Mais lento (devido à transformação) | Mais rápido (carga direta) |
| **Volume de Dados** | Ideal para volumes pequenos/médios | Projetado para Petabytes e Big Data |
| **Manutenção** | Alta (mudanças na fonte quebram o fluxo) | Baixa (o dado bruto está sempre disponível) |

*Fonte das informações: Indicium Academy, AWS, Databricks.*

![Arquitetura ETL e ELT](images/ETL-ELT.png)

---

## 🏗️ Repositórios de Dados: Warehouse vs. Lake vs. Lakehouse

A escolha da arquitetura de armazenamento define como uma empresa consegue processar, governar e extrair valor de seus ativos de dados.

### 1. Data Warehouse (DW)
Um repositório centralizado projetado especificamente para análise e relatórios de negócios.

* **Funcionamento:** Armazena dados que já foram extraídos, limpos e transformados (processo tradicional de ETL). Ele utiliza uma estrutura de "schema-on-write", o que significa que os dados devem ser organizados em um formato pré-definido antes de serem inseridos.
* **Características Principais:**
    * **Dados Estruturados:** Foca em dados altamente processados e organizados em tabelas.
    * **Performance Analítica:** Otimizado para consultas SQL complexas e rápidas.
    * **Governança Forte:** Oferece alto controle sobre quem acessa o quê e garante a integridade dos dados.
* **Uso Ideal:** Business Intelligence (BI), relatórios executivos e análise de dados históricos estruturados.

### 2. Data Lake
Um repositório vasto que armazena dados em seu formato bruto e nativo.

* **Funcionamento:** Aceita qualquer tipo de dado (estruturado, semiestruturado ou não estruturado) sem a necessidade de tratamento prévio. Ele utiliza o conceito de "schema-on-read", onde a estrutura é aplicada apenas quando o dado é lido para análise.
* **Características Principais:**
    * **Versatilidade:** Armazena desde logs de servidores e arquivos CSV até imagens e vídeos.
    * **Baixo Custo:** Geralmente utiliza armazenamento em nuvem de baixo custo para grandes volumes de dados.
    * **Escalabilidade:** Projetado para lidar com petabytes de informações de forma flexível.
* **Uso Ideal:** Ciência de Dados, Machine Learning, Big Data e armazenamento de longo prazo de dados brutos.

### 3. Data Lakehouse
Uma arquitetura híbrida que combina os melhores elementos do Data Warehouse e do Data Lake em uma única plataforma.

* **Funcionamento:** Implementa estruturas de dados e funções de gerenciamento de dados similares às de um DW (como transações ACID) diretamente sobre o armazenamento de baixo custo de um Data Lake.
* **Características Principais:**
    * **Unificação:** Elimina a necessidade de manter sistemas separados para BI e Machine Learning.
    * **Suporte a Transações ACID:** Garante que múltiplas partes possam ler e escrever dados simultaneamente sem erros.
    * **Esquemas Abertos:** Utiliza formatos de arquivos abertos (como Parquet ou Delta Lake) que podem ser lidos por diversas ferramentas.
* **Uso Ideal:** Empresas que buscam uma "fonte única da verdade" para engenharia de dados, ciência de dados e análises em tempo real.

---

### 📊 Tabela Comparativa

| Característica | Data Warehouse | Data Lake | Data Lakehouse |
| :--- | :--- | :--- | :--- |
| **Tipo de Dado** | Estruturado apenas | Estruturado e não estruturado | Todos os tipos (unificado) |
| **Esquema** | Schema-on-write (Rígido) | Schema-on-read (Flexível) | Gerenciamento de esquema (Híbrido) |
| **Custo** | Relativamente alto | Baixo | Baixo (preço de lake) |
| **Público Principal** | Analistas de BI e Negócios | Cientistas de Dados | Engenheiros, Analistas e Cientistas |

*Fontes: IBM, Microsoft Azure, Databricks.*

![Data Warehouse, lake e lakehouse](images/DW-DL-DLH.png)

---

## 🏗️ Modelagem Dimensional: Metodologia Kimball e Estruturas de Dados

A modelagem dimensional é o processo de organizar dados para facilitar a análise e melhorar a performance de consultas em ambientes OLAP. O objetivo é criar um "mapa" que os usuários de negócio consigam entender intuitivamente.

### 1. Metodologia Kimball (The Kimball Group)
Desenvolvida por Ralph Kimball, esta metodologia adota uma abordagem "bottom-up" (de baixo para cima), focando nos processos de negócio para construir o Data Warehouse.

* **Os 4 Passos do Design Dimensional:**
    1. **Selecionar o Processo de Negócio:** (Ex: Vendas, Pedidos, Logística).
    2. **Declarar o Grão:** Definir o nível de detalhe (Ex: Uma linha por item vendido por cupom fiscal).
    3. **Identificar as Dimensões:** Os substantivos da análise (Quem, Onde, Quando, O quê).
    4. **Identificar as Fatos:** As métricas quantitativas (Quanto, Valor, Quantidade).
* **Conceito Chave:** A modelagem deve ser centrada na facilidade de uso pelo analista e na performance de leitura.

### 2. Star Schema (Esquema Estrela)
É a arquitetura mais simples e amplamente utilizada em Modern Data Stack.

* **Estrutura:** Uma tabela **Fato** central conectada diretamente a várias tabelas **Dimensão**.
* **Características:**
    * **Desnormalização:** As dimensões não são normalizadas, o que significa que há redundância de dados para evitar JOINS complexos.
    * **Performance:** Excelente para consultas analíticas, pois exige menos junções entre tabelas.
    * **Uso Ideal:** Praticamente todos os Data Warehouses modernos (Snowflake, BigQuery).

#### 1. A Tabela Fato (O "O quê" e "Quanto")
A Tabela Fato é o centro do Star Schema. Ela registra os eventos quantitativos de um processo de negócio.

* **Granularidade (Grain):** É a definição do que uma única linha na tabela representa. Exemplo: "Uma linha por item vendido em cada transação". Definir o grão é o passo mais crítico da modelagem.
* **Chaves Estrangeiras (FKs):** A Fato não contém nomes ou descrições; ela contém IDs que se conectam às Dimensões.
* **Tipos de Medidas (Fatos):**
    * **Aditivas:** Podem ser somadas em todas as dimensões (Ex: Valor total da venda).
    * **Semi-aditivas:** Podem ser somadas em algumas dimensões, mas não em todas (Ex: Saldo bancário pode ser somado por região, mas não por tempo/datas).
    * **Não aditivas:** Geralmente proporções ou razões que não podem ser somadas (Ex: Margem de lucro unitária).

#### 2. Tabelas Dimensão (O "Quem", "Onde" e "Quando")
As Dimensões fornecem o contexto descritivo para os fatos. Elas são "chatas e largas", contendo muitas colunas de texto.

* **Atributos:** São as colunas de texto usadas para filtrar e agrupar nos relatórios (Ex: Nome do Produto, Categoria, Marca, Cor).
* **Surrogate Keys (Chaves Substitutas):** Em vez de usar o ID original do sistema (Natural Key), usa-se uma chave numérica simples criada pelo Data Warehouse. Isso é essencial para lidar com SCDs e performance.
* **Desnormalização:** Ao contrário dos bancos OLTP, aqui as tabelas são "achatadas". Não criamos uma tabela separada para 'Categoria'; colocamos o nome da categoria diretamente na tabela de 'Produto' para evitar Joins.

### 3. Snowflake Schema (Esquema Floco de Neve)
Uma variação do Star Schema onde as tabelas de dimensão são normalizadas.

* **Estrutura:** As dimensões se ramificam em sub-dimensões (Ex: A dimensão 'Produto' se conecta a uma dimensão 'Categoria').
* **Características:**
    * **Normalização:** Reduz a redundância e economiza espaço de armazenamento.
    * **Complexidade:** Exige mais JOINS, o que pode impactar a performance e tornar o SQL mais difícil de ler.
* **Uso Ideal:** Cenários onde o custo de armazenamento é extremamente alto ou quando a hierarquia dos dados é muito complexa.

### 4. SCD (Slowly Changing Dimensions)
As "Dimensões que Mudam Lentamente" descrevem como o sistema lida com alterações nos atributos das dimensões ao longo do tempo.

* **Tipos Mais Importantes:**

| Tipo | Nome | Funcionamento | Uso Ideal |
| :--- | :--- | :--- | :--- |
| **Tipo 0** | Fixo | O valor original é mantido para sempre. Alterações no sistema de origem são ignoradas. | Dados imutáveis como "Data de Nascimento" ou "ID Original". |
| **Tipo 1** | Sobrescrita | O valor antigo é apagado e o novo é inserido por cima. Perde-se o histórico. | Correção de erros ou quando o histórico não tem valor (Ex: Corrigir erro de grafia). |
| **Tipo 2** | Histórico por Linha | Cria-se uma nova linha para o registro. Usa-se colunas `data_inicio`, `data_fim` e `versao_atual` (booleano). | **Padrão Ouro.** Essencial quando o histórico importa (Ex: Onde o cliente morava quando fez a compra X?). |
| **Tipo 3** | Histórico por Coluna | Cria-se uma nova coluna chamada `valor_anterior`. Mantém apenas a versão atual e a imediatamente anterior. | Quando você só precisa comparar o "agora" com o "antes" de forma rápida. |
| **Tipo 4** | Tabela de Histórico | A tabela principal mantém apenas o dado atual (Tipo 1), mas todas as mudanças são gravadas em uma tabela de "log" separada. | Quando a tabela de dimensão é gigantesca e muda com muita frequência. |
| **Tipo 6** | Híbrido (1+2+3) | Combina técnicas: usa o Tipo 2 para rastrear histórico, mas também colunas do Tipo 3 para acesso rápido. (2+3+1 = 6). | Relatórios de altíssima complexidade que exigem visão atual e histórica na mesma linha. |

---

### 📊 Comparativo: Star vs. Snowflake

| Característica | Star Schema | Snowflake Schema |
| :--- | :--- | :--- |
| **Normalização** | Desnormalizado | Normalizado |
| **Complexidade de Query** | Baixa (Menos Joins) | Alta (Mais Joins) |
| **Integridade de Dados** | Menor (Risco de redundância) | Maior (Estrutura rígida) |
| **Performance de Leitura** | Superior | Inferior |

*Fontes: Microsoft Learn, IBM Architecture, dbt Labs Documentation, The Data Warehouse Toolkit (Kimball).*

---
