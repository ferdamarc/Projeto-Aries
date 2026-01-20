import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Tema visual
TEMA = {
    'mapa': px.colors.sequential.Blues,
    'barras': '#2ecc71',
    'linha': '#e74c3c'
}

# --- INÍCIO: Carregar dados dos municípios de SP ---
MUNICIPIOS_SP_PATH = r'c:\Users\Fernando\Documents\CEPID - Projeto ARIES\Aries-Project\ibge\DTB_2023\municipiosSP.csv' # Use o caminho correto
municipios_sp_map = {}
try:
    df_municipios_sp = pd.read_csv(
        MUNICIPIOS_SP_PATH,
        sep=';',
        header=0, # Indica que a primeira linha é o cabeçalho
        usecols=['Código Município Completo', 'Nome_Município'], # Usa os nomes das colunas
        dtype={'Código Município Completo': int, 'Nome_Município': str}
    )
    # Cria um dicionário: {codigo_ibge: nome_municipio}
    municipios_sp_map = pd.Series(
        df_municipios_sp.Nome_Município.values, # Usa o nome correto da coluna
        index=df_municipios_sp['Código Município Completo'] # Usa o nome correto da coluna
    ).to_dict()
except FileNotFoundError:
    st.warning(f"Arquivo de municípios não encontrado em: {MUNICIPIOS_SP_PATH}. Nomes dos municípios de SP não serão exibidos.")
except Exception as e:
    st.error(f"Erro ao carregar arquivo de municípios: {e}")
# --- FIM: Carregar dados dos municípios de SP ---

# Dicionário para mapear códigos de UF para nomes e siglas
UFS = {
    11: {'nome': 'Rondônia', 'sigla': 'RO'},
    12: {'nome': 'Acre', 'sigla': 'AC'},
    13: {'nome': 'Amazonas', 'sigla': 'AM'},
    14: {'nome': 'Roraima', 'sigla': 'RR'},
    15: {'nome': 'Pará', 'sigla': 'PA'},
    16: {'nome': 'Amapá', 'sigla': 'AP'},
    17: {'nome': 'Tocantins', 'sigla': 'TO'},
    21: {'nome': 'Maranhão', 'sigla': 'MA'},
    22: {'nome': 'Piauí', 'sigla': 'PI'},
    23: {'nome': 'Ceará', 'sigla': 'CE'},
    24: {'nome': 'Rio Grande do Norte', 'sigla': 'RN'},
    25: {'nome': 'Paraíba', 'sigla': 'PB'},
    26: {'nome': 'Pernambuco', 'sigla': 'PE'},
    27: {'nome': 'Alagoas', 'sigla': 'AL'},
    28: {'nome': 'Sergipe', 'sigla': 'SE'},
    29: {'nome': 'Bahia', 'sigla': 'BA'},
    31: {'nome': 'Minas Gerais', 'sigla': 'MG'},
    32: {'nome': 'Espírito Santo', 'sigla': 'ES'},
    33: {'nome': 'Rio de Janeiro', 'sigla': 'RJ'},
    35: {'nome': 'São Paulo', 'sigla': 'SP'},
    41: {'nome': 'Paraná', 'sigla': 'PR'},
    42: {'nome': 'Santa Catarina', 'sigla': 'SC'},
    43: {'nome': 'Rio Grande do Sul', 'sigla': 'RS'},
    50: {'nome': 'Mato Grosso do Sul', 'sigla': 'MS'},
    51: {'nome': 'Mato Grosso', 'sigla': 'MT'},
    52: {'nome': 'Goiás', 'sigla': 'GO'},
    53: {'nome': 'Distrito Federal', 'sigla': 'DF'}
}

def render(data):
    """
    Dashboard de Análise Geográfica
    """

    st.header("🏥 Análise Geográfica de Internações", divider='rainbow')
    
    with st.sidebar:
        anos_disponiveis = sorted(data['dim_tempo']['ANO_CMPT'].unique())
        ano_selecionado = st.selectbox("Ano:", anos_disponiveis, index=len(anos_disponiveis)-1)
        
        nivel_geografico = st.radio(
            "Nível de análise:",
            ["Estado", "Município"]
        )
        
        uf_filtro = None
        if nivel_geografico == "Município":
            ufs_disponiveis = sorted(data['dim_localizacao']['UF_RES'].unique())
            opcoes_uf = {
                (UFS.get(uf, {}).get('nome', f'UF {uf}')): uf 
                for uf in ufs_disponiveis if uf in UFS
            }
            
            if opcoes_uf:
                uf_selecionada = st.selectbox(
                    "Estado para análise municipal:",
                    list(opcoes_uf.keys())
                )
                uf_filtro = opcoes_uf.get(uf_selecionada)

    df_filtrado = (
        data['fato']
        .merge(data['dim_tempo'][data['dim_tempo']['ANO_CMPT'] == ano_selecionado], on='ID_TEMPO')
        .merge(data['dim_localizacao'], on='ID_LOCALIZACAO')
    )

    # Removando as duplicadas de dados provindos de merge
    # 'N_AIH' deve ser único por internação.
    chave_primaria = ['N_AIH'] 
    duplicados_antes = df_filtrado.duplicated(subset=chave_primaria).sum()
    
    if duplicados_antes > 0:
        df_filtrado = df_filtrado.drop_duplicates(subset=chave_primaria, keep='first')
    
    # Garante que MUNIC_RES seja numérico para o merge/map
    df_filtrado['MUNIC_RES'] = pd.to_numeric(df_filtrado['MUNIC_RES'], errors='coerce') # Se algum valor n puder ser convertido, ele será NaN
    df_filtrado.dropna(subset=['MUNIC_RES'], inplace=True) # Remove linhas onde MUNIC_RES é NaN
    
    df_filtrado['MUNIC_RES'] = df_filtrado['MUNIC_RES'].astype(int)

    if nivel_geografico == "Município" and uf_filtro is not None:
        df_filtrado = df_filtrado[df_filtrado['UF_RES'] == uf_filtro]
    
    if nivel_geografico == "Estado":
        df_filtrado['nome_uf'] = df_filtrado['UF_RES'].apply(
            lambda x: UFS.get(x, {}).get('nome', f'UF {x}')
        )
        df_filtrado['sigla_uf'] = df_filtrado['UF_RES'].apply(
            lambda x: UFS.get(x, {}).get('sigla', str(x))
        )
        group_col = 'nome_uf'
        location_col = 'sigla_uf'
        col_name = 'Estado'
    else: # Nível Município
        # Aplica o mapeamento apenas se for SP (35) e o mapa foi carregado
        if uf_filtro == 35 and municipios_sp_map:
            df_filtrado['nome_municipio'] = df_filtrado['MUNIC_RES'].map(municipios_sp_map)
            # Se algum município não for encontrado no mapa, usa o código como fallback
            df_filtrado['nome_municipio'].fillna(df_filtrado['MUNIC_RES'].astype(str) + ' (Código não encontrado)', inplace=True)
            group_col = 'nome_municipio'
        else:
            # Para outros estados ou se o mapa falhou, usa o código
            df_filtrado['nome_municipio'] = df_filtrado['MUNIC_RES'].astype(str)
            group_col = 'MUNIC_RES' # Agrupa pelo código original

        location_col = group_col # Usar a mesma coluna para localização no gráfico/tabela
        col_name = 'Município'
    
    df_geo = df_filtrado.groupby(group_col).agg(
        total_internacoes=('N_AIH', 'count'),
        custo_total=('VAL_TOT', 'sum'),
        permanencia_media=('DIAS_PERMANENCIA', 'mean'),
        mortalidade=('MORTE', 'mean')
    ).reset_index()
    
    if nivel_geografico == "Estado":
        df_geo['location'] = df_filtrado.groupby(group_col)['sigla_uf'].first().reset_index()['sigla_uf']
    else: # Nível Município
        # A coluna 'location' agora é a mesma que 'group_col' (nome ou código)
        df_geo['location'] = df_geo[group_col] 
    
    df_geo['mortalidade'] = df_geo['mortalidade'] * 100

    st.subheader(f"Distribuição de Internações por {nivel_geografico} em {ano_selecionado}")
    
    if nivel_geografico == "Estado":
        try:
            fig = px.choropleth(
                df_geo,
                locations='location',
                locationmode='ISO-3',
                color='total_internacoes',
                color_continuous_scale=TEMA['mapa'],
                scope="south america",
                title=f"Total de Internações por Estado ({ano_selecionado})",
                labels={
                    'total_internacoes': 'Total de Internações',
                    'location': 'Estado'
                }
            )
            
            fig.update_geos(
                showcountries=False,
                showcoastlines=True,
                showland=True,
                fitbounds="locations",
                visible=False,
                landcolor='lightgray'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao criar mapa: {str(e)}")
            usar_barras = True
        
    else:
        usar_barras = True
    
    if nivel_geografico != "Estado" or 'usar_barras' in locals():
        df_top = df_geo.sort_values('total_internacoes', ascending=False).head(15)
        
        fig = px.bar(
            df_top,
            x=group_col, # Usará nome do município se for SP, senão código
            y='total_internacoes',
            color='total_internacoes',
            color_continuous_scale=TEMA['mapa'],
            title=f"Top 15 {nivel_geografico}s com Maior Número de Internações ({ano_selecionado})",
            labels={
                group_col: col_name, # Rótulo dinâmico
                'total_internacoes': 'Total de Internações'
            }
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(f"Análise Detalhada por {nivel_geografico}")
    
    locais_disponiveis = df_geo.sort_values('total_internacoes', ascending=False)[group_col].tolist()
    
    if locais_disponiveis:
        local_selecionado = st.selectbox(
            f"Selecione um {nivel_geografico.lower()} para detalhes:",
            locais_disponiveis
        )
        
        dados = df_geo[df_geo[group_col] == local_selecionado].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Internações", f"{int(dados['total_internacoes']):,}")
        col2.metric("Custo Total", f"R$ {dados['custo_total']:,.2f}")
        col3.metric("Permanência Média", f"{dados['permanencia_media']:.1f} dias")
        col4.metric("Taxa de Mortalidade", f"{dados['mortalidade']:.2f}%")
        
        if nivel_geografico == "Estado" and len(df_filtrado) > 0:
            st.subheader(f"Principais Municípios de {local_selecionado}")
            
            codigo_uf_selecionado = next((uf for uf, info in UFS.items() if info['nome'] == local_selecionado), None)
            
            if codigo_uf_selecionado:
                df_municipios = df_filtrado[df_filtrado['UF_RES'] == codigo_uf_selecionado].copy() # Usar cópia para evitar SettingWithCopyWarning
                
                # Garante tipo numérico para merge/map futuro se necessário
                df_municipios['MUNIC_RES'] = pd.to_numeric(df_municipios['MUNIC_RES'], errors='coerce').astype('Int64') 

                df_mun = df_municipios.groupby('MUNIC_RES').agg(
                    total_internacoes=('N_AIH', 'count'),
                    custo_total=('VAL_TOT', 'sum')
                ).reset_index()

                # Adiciona nomes dos municípios se for SP
                mun_label_col = 'MUNIC_RES'
                mun_x_label = 'Código do Município'
                if codigo_uf_selecionado == 35 and municipios_sp_map:
                    df_mun['nome_municipio'] = df_mun['MUNIC_RES'].map(municipios_sp_map)
                    df_mun['nome_municipio'].fillna(df_mun['MUNIC_RES'].astype(str) + ' (Código)', inplace=True)
                    mun_label_col = 'nome_municipio'
                    mun_x_label = 'Município'
                else:
                     # Converte código para string para exibição no gráfico
                    df_mun['MUNIC_RES'] = df_mun['MUNIC_RES'].astype(str)


                df_top_mun = df_mun.sort_values('total_internacoes', ascending=False).head(10)
                
                fig = px.bar(
                    df_top_mun,
                    x=mun_label_col, # Usa nome ou código dependendo do estado
                    y='total_internacoes',
                    color='total_internacoes',
                    title=f"Top 10 Municípios de {local_selecionado} por Internações",
                    labels={
                        mun_label_col: mun_x_label, # Rótulo dinâmico
                        'total_internacoes': 'Total de Internações'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)

    with st.expander("Ver tabela de dados completa"):
        df_display = df_geo.copy()
        df_display['permanencia_media'] = df_display['permanencia_media'].round(2).astype(str) + ' dias'
        df_display['custo_total'] = df_display['custo_total'].apply(lambda x: f"R$ {x:,.2f}")
        df_display['mortalidade'] = df_display['mortalidade'].round(2).astype(str) + '%'
        
        df_display = df_display.rename(columns={
            group_col: col_name, # Renomeia a coluna (que pode ser nome ou código)
            'total_internacoes': 'Total de Internações',
            'custo_total': 'Custo Total',
            'permanencia_media': 'Permanência Média',
            'mortalidade': 'Taxa de Mortalidade'
        }).drop(columns=['location']) # Remove a coluna 'location' duplicada
        
        st.dataframe(df_display, use_container_width=True)

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from dashboard import carregar_dados
    render(carregar_dados())