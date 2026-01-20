import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def render(data):
    """
    Renderiza a página de Análise de Custos do Dashboard.
    
    Parâmetros:
    data: Dicionário contendo os dataframes do modelo dimensional
    """
    st.header("Análise de Custos das Internações")
    
    st.sidebar.subheader("Filtros para Análise de Custos")
    
    # Verificar se temos dados suficientes
    if 'dim_tempo' not in data or data['dim_tempo'].empty:
        st.warning("Não há dados temporais disponíveis para análise.")
        return
    
    # Extrair anos disponíveis de forma segura
    try:
        anos_disponiveis = sorted(data['dim_tempo']['ANO_CMPT'].unique())
        
        # Verificar se há anos disponíveis
        if len(anos_disponiveis) == 0:
            st.warning("Não há dados de anos disponíveis para análise de custos.")
            return
        
        # Verificar se temos mais de um ano para criar um intervalo
        if len(anos_disponiveis) == 1:
            st.sidebar.info(f"Apenas dados do ano {anos_disponiveis[0]} estão disponíveis.")
            ano_inicial = ano_final = anos_disponiveis[0]
        else:
            # Só criar o slider se tivermos anos diferentes
            ano_inicial, ano_final = st.sidebar.select_slider(
                "Selecione o intervalo de anos:",
                options=anos_disponiveis,
                value=(anos_disponiveis[0], anos_disponiveis[-1])
            )
    except Exception as e:
        st.error(f"Erro ao processar anos disponíveis: {str(e)}")
        return
    
    dimensao_analise = st.sidebar.selectbox(
        "Dimensão para análise:",
        ["Diagnósticos", "Hospitais", "Regiões", "Procedimentos", "Faixa Etária"]
    )
    
    # Filtrar dados de forma segura
    try:
        # Criar filtro SQL-like para evitar problemas com merge
        fato_filtrado = data['fato'].merge(
            data['dim_tempo'][
                (data['dim_tempo']['ANO_CMPT'] >= ano_inicial) & 
                (data['dim_tempo']['ANO_CMPT'] <= ano_final)
            ],
            on='ID_TEMPO'
        )
        
        # Verificar se temos dados após a filtragem
        if fato_filtrado.empty:
            st.warning(f"Não há dados disponíveis para o intervalo de {ano_inicial} a {ano_final}.")
            return
    except Exception as e:
        st.error(f"Erro ao filtrar dados por ano: {str(e)}")
        return
    
    st.subheader("Estatísticas Gerais de Custos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    custo_total = fato_filtrado['VAL_TOT'].sum()
    if custo_total >= 1e9:
        valor_formatado = f"R$ {custo_total/1e9:.2f} bi"
    elif custo_total >= 1e6:
        valor_formatado = f"R$ {custo_total/1e6:.2f} mi"
    else:
        valor_formatado = f"R$ {custo_total:,.2f}"
        
    col1.metric(
        label="Custo Total", 
        value=valor_formatado
    )
    
    custo_medio = fato_filtrado['VAL_TOT'].mean()
    col2.metric(
        label="Custo Médio por Internação", 
        value=f"R$ {custo_medio:,.2f}"
    )
    
    dias_validos = fato_filtrado[fato_filtrado['DIAS_PERMANENCIA'] > 0]
    if len(dias_validos) > 0:
        custo_por_dia = dias_validos['VAL_TOT'].sum() / dias_validos['DIAS_PERMANENCIA'].sum()
    else:
        custo_por_dia = 0
    
    col3.metric(
        label="Custo Médio por Dia", 
        value=f"R$ {custo_por_dia:,.2f}"
    )
    
    total_internacoes = len(fato_filtrado)
    col4.metric(
        label="Total de Internações", 
        value=f"{total_internacoes:,}"
    )