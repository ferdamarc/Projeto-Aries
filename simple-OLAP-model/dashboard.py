import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from modules.visao_geral import render as render_visao_geral
from modules.analise_temporal import render as render_analise_temporal
from modules.analise_geografica_copy import render as render_analise_geografica
from modules.analise_diagnosticos import render as render_analise_diagnosticos
from modules.analise_custos import render as render_analise_custos
from modules.analise_desfechos import render as render_analise_desfechos
from modules.consultas_doenca import render as render_consultas_doenca

st.set_page_config(
    page_title="Dashboard SIH/SUS", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def carregar_dados():
    """
    Carrega os dados processados do SIH de arquivos CSV. 
    Futuramente, será adaptado para carregar de um banco de dados. 
    Utiliza cache para melhor performance. 
    """
    
    # Teste com arquivos de uma mesmo ano
    # base_dir = r'C:\Users\Fernando\Documents\CEPID - Projeto ARIES\Aries-Project\data\processados\SIH\Teste'
    
    # Teste com um arquivo que contém 200 internações em cada mês (fevereiro)
    base_dir = r'C:\Users\Fernando\Documents\CEPID - Projeto ARIES\Aries-Project\data\processados\SIH'
    
    fato = pd.read_csv(f'{base_dir}/fato_internacao.csv', sep=';')
    dim_tempo = pd.read_csv(f'{base_dir}/dim_tempo.csv', sep=';')
    dim_paciente = pd.read_csv(f'{base_dir}/dim_paciente.csv', sep=';')
    dim_hospital = pd.read_csv(f'{base_dir}/dim_hospital.csv', sep=';')
    dim_localizacao = pd.read_csv(f'{base_dir}/dim_localizacao.csv', sep=';')
    dim_diagnostico = pd.read_csv(f'{base_dir}/dim_diagnostico.csv', sep=';')
    dim_procedimento = pd.read_csv(f'{base_dir}/dim_procedimento.csv', sep=';')
    
    # Converter datas
    fato['DT_INTER'] = pd.to_datetime(fato['DT_INTER'])
    fato['DT_SAIDA'] = pd.to_datetime(fato['DT_SAIDA'])
    
    return {
        'fato': fato,
        'dim_tempo': dim_tempo,
        'dim_paciente': dim_paciente,
        'dim_hospital': dim_hospital,
        'dim_localizacao': dim_localizacao,
        'dim_diagnostico': dim_diagnostico,
        'dim_procedimento': dim_procedimento
    }


def main():
    st.title("Dashboard de Análise de Internações SUS")
    st.markdown("### Modelo Dimensional OLAP para dados do SIH/SUS")
    
    with st.spinner('Carregando dados...'):
        data = carregar_dados()
    
    st.sidebar.header("Configurações")
    
    menu = st.sidebar.radio(
        "Selecione a análise:",
        ["Visão Geral", "Análise Temporal", "Análise Geográfica", 
         "Análise de Diagnósticos", "Análise de Custos", "Análise de Desfechos",
         "Consulta por Doença Específica"]
    )
    
    # Estatísticas gerais sempre mostradas no topo
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric(
            label="Total de Internações", 
            value=f"{len(data['fato']):,}"
        )
        
        # Format value based on magnitude (thousands, millions, billions)
        valor_total = data['fato']['VAL_TOT'].sum()
        if valor_total >= 1e9:  # billions
            valor_formatado = f"R$ {valor_total/1e9:.1f} B"
        elif valor_total >= 1e6:  # millions
            valor_formatado = f"R$ {valor_total/1e6:.1f} M"
        elif valor_total >= 1e3:  # thousands
            valor_formatado = f"R$ {valor_total/1e3:.1f} K"
        else:
            valor_formatado = f"R$ {valor_total:.2f}"

        col2.metric(
            label="Valor Total", 
            value=valor_formatado
        )
        
        col3.metric(
            label="Permanência Média", 
            value=f"{data['fato']['DIAS_PERMANENCIA'].mean():.1f} dias"
        )
        
        col4.metric(
            label="Taxa de Mortalidade", 
            value=f"{(data['fato']['MORTE'].mean() * 100):.2f}%"
        )
    
    st.markdown("---")
    
    # Renderizar diferentes seções com base na seleção do menu
    if menu == "Visão Geral":
        render_visao_geral(data)
    
    elif menu == "Análise Temporal":
        render_analise_temporal(data)
    
    elif menu == "Análise Geográfica":
        render_analise_geografica(data)
    
    elif menu == "Análise de Diagnósticos":
        render_analise_diagnosticos(data)
    
    elif menu == "Análise de Custos":
        render_analise_custos(data)
    
    elif menu == "Análise de Desfechos":
        render_analise_desfechos(data)
    
    elif menu == "Consulta por Doença Específica":
        render_consultas_doenca(data)

if __name__ == '__main__':
    main()