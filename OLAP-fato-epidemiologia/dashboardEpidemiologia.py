import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard Epidemiológico",
    page_icon="🦠",
    layout="wide"
)

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Fernando\Documents\CEPID - Projeto ARIES\Aries-Project\OLAP-fato-epidemiologia\bruto_20_amostras.csv", sep=',', encoding='latin1')
    
    # Converter datas e calcular dias de permanência
    df['DT_INTER'] = pd.to_datetime(df['DT_INTER'], format='%Y%m%d')
    df['DT_SAIDA'] = pd.to_datetime(df['DT_SAIDA'], format='%Y%m%d')
    df['DIAS_PERM'] = (df['DT_SAIDA'] - df['DT_INTER']).dt.days
    
    return df

df = load_data()

# Sidebar - Filtros
st.sidebar.header("Filtros")
selected_diagnosis = st.sidebar.selectbox(
    "Selecione o CID-10 Principal",
    options=df['DIAG_PRINC'].unique()
)

selected_municipio = st.sidebar.selectbox(
    "Selecione o Município",
    options=df['MUNIC_RES'].unique()
)

# Seção 1: Métricas Principais
st.header("Visão Geral Epidemiológica")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Casos", len(df))
with col2:
    st.metric("Taxa de Mortalidade", f"{df['MORTE'].mean()*100:.1f}%")
with col3:
    st.metric("Média Dias Internação", f"{df['DIAS_PERM'].mean():.1f}")
with col4:
    st.metric("Casos com Infecção Hospitalar", df['INFEHOSP'].sum())

st.divider()

# Seção 2: Análise Temporal
st.header("Tendência Temporal de Casos")
df['MES_ANO'] = df['DT_INTER'].dt.to_period('M').astype(str)

fig_temporal = px.line(
    df.groupby('MES_ANO')['N_AIH'].count().reset_index(),
    x='MES_ANO',
    y='N_AIH',
    title="Casos por Mês"
)
st.plotly_chart(fig_temporal, use_container_width=True)

# Seção 3: Distribuição Geográfica
st.header("Distribuição Geográfica")
fig_geo = px.bar(
    df.groupby('MUNIC_RES')['N_AIH'].count().reset_index().sort_values(by='N_AIH', ascending=False).head(10),
    x='MUNIC_RES',
    y='N_AIH',
    title="Top 10 Municípios por Casos"
)
st.plotly_chart(fig_geo, use_container_width=True)

# Seção 4: Análise Demográfica
st.header("Perfil Demográfico")
col1, col2 = st.columns(2)

with col1:
    fig_idade = px.histogram(
        df,
        x='IDADE',
        title="Distribuição por Idade"
    )
    st.plotly_chart(fig_idade, use_container_width=True)

with col2:
    fig_sexo = px.pie(
        df,
        names='SEXO',
        title="Distribuição por Sexo",
        hole=0.4
    )
    st.plotly_chart(fig_sexo, use_container_width=True)

# Seção 5: Detalhamento por Doença
st.header(f"Análise Detalhada: {selected_diagnosis}")
filtered_df = df[df['DIAG_PRINC'] == selected_diagnosis]

if not filtered_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Estatísticas Chave")
        st.metric("Casos Totais", len(filtered_df))
        st.metric("Mortalidade", f"{filtered_df['MORTE'].mean()*100:.1f}%")
        st.metric("Comorbidade Mais Comum", filtered_df['DIAG_SECUN'].mode()[0])
    
    with col2:
        fig_comorbidades = px.bar(
            filtered_df['DIAG_SECUN'].value_counts().reset_index(),
            x='count',
            y='DIAG_SECUN',
            title="Comorbidades Associadas"
        )
        st.plotly_chart(fig_comorbidades, use_container_width=True)
else:
    st.warning("Nenhum caso encontrado para este diagnóstico.")

st.divider()
st.caption("Dados: SIH/SUS | Desenvolvido com Streamlit")