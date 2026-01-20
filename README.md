# Projeto ARIES - ETL Process for SIH/SUS Data in a DataLake House

## Informações Gerais do Projeto
- **Bolsista:** Fernando Daniel Marcelino
- **Orientador:** Prof. Dr. Elbert Einstein Nehrer Macau
- **Coorientadora:** Profa. Dra. Daniela Leal Musa
- **Instituição:** Universidade Federal de São Paulo - Instituto de Ciência e Tecnologia
- **Grupo de Pesquisa:** CEPID - ARIES (Centros de Pesquisa, Inovação e Difusão - Instituto Paulista de Resistência aos Antimicrobianos)
- **Instituição de Fomento:** FAPESP (Fundação de Amparo à Pesquisa do Estado de São Paulo)

## Visão Geral
Este é um projeto de Iniciação Científica amparado pela FAPESP (Fundação de Amparo à Pesquisa do Estado de São Paulo) que desenvolve um processo ETL (Extract, Transform, Load) para integração de dados do SIH/SUS (Sistema de Informações Hospitalares do Sistema Único de Saúde) em um Data Lake House. O objetivo principal é criar uma estrutura robusta para análise de dados relacionados à resistência antimicrobiana (RAM) em hospitais públicos brasileiros.

## Contextualização e Motivação
A resistência antimicrobiana tem se tornado um dos maiores desafios de saúde pública mundial. Estima-se que cerca de 7,7 milhões de pessoas morrem todos os anos devido a infecções bacterianas, e as previsões indicam que esse número pode chegar a 10 milhões até 2050. Este projeto visa utilizar dados do SIH/SUS para obter informações sobre a incidência e distribuição de resistência antimicrobiana nos hospitais públicos brasileiros.

## Objetivos
- Desenvolver um processo ETL para integrar dados do SIH/SUS em um Data Lake House.
- Garantir a qualidade e integridade dos dados durante o processo de ETL.
- Otimizar o armazenamento e o tempo de consultas dos dados.
- Criar um ambiente de desenvolvimento e produção para o processo ETL.
- Facilitar a análise de dados e a geração de relatórios sobre resistência antimicrobiana.

## Tecnologias Utilizadas
- **Linguagem de Programação:** Python 3.10
- **Banco de Dados:** PostgreSQL com PgAdmin 4
- **Bibliotecas Principais:**
    - PySUS (API para acesso aos dados do DATASUS)
    - Pandas (manipulação de dados)
    - SQLAlchemy (integração com banco de dados)
    - Streamlit (interface de relatórios)
    - Schedule (agendamento de tarefas)

## Resultados Obtidos
- Desenvolvimento de um processo ETL funcional para integração de dados do SIH/SUS.
- Criação de um Data Lake House com dados estruturados e prontos para análise.
- Implementação de um ambiente de desenvolvimento e produção para o processo ETL.
- Geração de relatórios e dashboards para visualização dos dados de resistência antimicrobiana.

## Como executar
1. Clone o repositório
2. Instale as dependências: pip install -r requirements.txt
3. Configure as conexões com o banco de dados
4. Execute os scripts de ETL para carregar os dados
5. Inicie o dashboard: streamlit run simple-OLAP-model/dashboard.py