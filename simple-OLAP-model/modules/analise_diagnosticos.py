import streamlit as st
import pandas as pd
import plotly.express as px

def render(data):
    st.header("📊 Análise de Diagnósticos", divider='rainbow')

    # --- 1. Filtros e Preparação de Dados Base ---
    with st.sidebar:
        st.subheader("⚙️ Filtros")
        anos_disponiveis = sorted(data['dim_tempo']['ANO_CMPT'].unique())
        if not anos_disponiveis:
            st.warning("Não há dados de ano disponíveis na dim_tempo.")
            return # Interrompe a execução se não houver anos

        ano_selecionado = st.selectbox(
            "Selecione o ano:",
            anos_disponiveis,
            index=len(anos_disponiveis) - 1 if anos_disponiveis else 0 # Padrão para o último ano
        )

    # DataFrame Base: Mescla inicial sem remover duplicatas ainda
    df_tempo_filtrado = data['dim_tempo'][data['dim_tempo']['ANO_CMPT'] == ano_selecionado]
    if df_tempo_filtrado.empty:
        st.warning(f"Não há dados de tempo para o ano {ano_selecionado}.")
        return

    df_base = (
        data['fato']
        .merge(df_tempo_filtrado, on='ID_TEMPO', how='inner')
        .merge(data['dim_diagnostico'], on='ID_DIAGNOSTICO', how='inner')
    )

    if df_base.empty:
        st.warning(f"Não foram encontrados dados de fatos para o ano {ano_selecionado} após mesclagem.")
        return

    # DataFrame para Contagem Única de Internações por Diagnóstico
    df_unique_internacoes = df_base.drop_duplicates(subset=['N_AIH', 'DIAG_PRINC'])

    if df_unique_internacoes.empty:
        st.warning(f"Não foram encontradas internações únicas para o ano {ano_selecionado}.")
        return

    # --- 2. Diagnósticos Mais Frequentes ---
    st.subheader("🔍 Diagnósticos Mais Frequentes")

    # Agregação: Contagem única de df_unique_internacoes, outras métricas de df_base
    diag_contagem = df_unique_internacoes.groupby('DIAG_PRINC').agg(
        internacoes=('N_AIH', 'nunique')
    ).reset_index()

    diag_metricas = df_base.groupby('DIAG_PRINC').agg(
        custo_total=('VAL_TOT', 'sum'),
        mortalidade_media=('MORTE', 'mean')
    ).reset_index()

    # Juntar contagem e métricas
    diagnosticos = pd.merge(diag_contagem, diag_metricas, on='DIAG_PRINC', how='left')
    diagnosticos = diagnosticos.sort_values('internacoes', ascending=False).fillna(0) # Ordenar e tratar NaNs
    
    # Criando um debug dentro da aplicação que mostra o dataframe filtrado
    st.write("DataFrame filtrado:", diagnosticos)

    if diagnosticos.empty:
        st.warning("Não foi possível calcular os diagnósticos mais frequentes.")
        return

    top_n = st.slider("Quantidade de diagnósticos a exibir:", min_value=5, max_value=min(50, len(diagnosticos)), value=min(10, len(diagnosticos)))
    df_top = diagnosticos.head(top_n)

    # Gráfico de Barras - Top N Diagnósticos
    fig_bar = px.bar(
        df_top,
        x='DIAG_PRINC',
        y='internacoes',
        labels={'DIAG_PRINC': 'Código CID-10', 'internacoes': 'Internações Únicas'},
        title=f'Top {top_n} Diagnósticos por Número de Internações Únicas ({ano_selecionado})',
        color='internacoes',
        color_continuous_scale=px.colors.sequential.Viridis,
        height=500
    )
    fig_bar.update_layout(xaxis_title='Código CID-10', yaxis_title='Internações Únicas')
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- 3. Histograma da Frequência de Internações por Diagnóstico ---
    st.subheader("📊 Distribuição da Frequência de Internações")
    fig_hist = px.histogram(
        diagnosticos,
        x='internacoes',
        nbins=max(20, top_n // 2), # Ajustar número de bins
        title=f'Histograma da Frequência de Internações por Diagnóstico ({ano_selecionado})',
        labels={'internacoes': 'Número de Internações Únicas por Diagnóstico'},
        opacity=0.8,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_hist.update_layout(
        yaxis_title='Quantidade de Diagnósticos',
        xaxis_title='Número de Internações Únicas por Diagnóstico'
    )
    st.plotly_chart(fig_hist, use_container_width=True)


    # --- 4. Detalhes por Diagnóstico Selecionado ---
    st.subheader("📈 Detalhes por Diagnóstico")

    if not df_top.empty:
        # Usar códigos CID do df_top que já está ordenado
        cid_selecionado = st.selectbox(
            "Selecione um diagnóstico do Top N para detalhes:",
            df_top['DIAG_PRINC'].tolist()
        )

        # Filtrar df_base para obter TODOS os dados do CID selecionado no ano
        df_cid_detalhes = df_base[df_base['DIAG_PRINC'] == cid_selecionado].copy() # Usar .copy() para evitar SettingWithCopyWarning

        if not df_cid_detalhes.empty:
            # Calcular métricas detalhadas usando df_cid_detalhes
            internacoes_unicas_cid = df_cid_detalhes['N_AIH'].nunique()
            custo_total_cid = df_cid_detalhes['VAL_TOT'].sum()
            mortalidade_media_cid = df_cid_detalhes['MORTE'].mean()
            permanencia_media_cid = df_cid_detalhes['DIAS_PERMANENCIA'].mean()

            # Garantir tratamento de NaN antes da formatação
            internacoes_unicas_cid = 0 if pd.isna(internacoes_unicas_cid) else int(internacoes_unicas_cid)
            custo_total_cid = 0.0 if pd.isna(custo_total_cid) else custo_total_cid
            mortalidade_media_cid = 0.0 if pd.isna(mortalidade_media_cid) else mortalidade_media_cid
            permanencia_media_cid = 0.0 if pd.isna(permanencia_media_cid) else permanencia_media_cid

            # Exibir métricas
            st.markdown(f"**Métricas para o Diagnóstico: {cid_selecionado} ({ano_selecionado})**")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Internações Únicas", f"{internacoes_unicas_cid:,}")
            col2.metric("Custo Total (R$)", f"{custo_total_cid:,.2f}")
            col3.metric("Mortalidade Média", f"{mortalidade_media_cid*100:.2f}%")
            col4.metric("Permanência Média", f"{permanencia_media_cid:.1f} dias")

            # Gráfico de Série Temporal Mensal para o CID selecionado
            st.markdown(f"**Evolução Mensal para {cid_selecionado} ({ano_selecionado})**")
            # Adicionar mês aos detalhes
            df_cid_detalhes['MES_CMPT'] = pd.to_datetime(df_cid_detalhes['DT_INTER'], errors='coerce').dt.month
            df_cid_detalhes = df_cid_detalhes.dropna(subset=['MES_CMPT']) # Remover linhas onde a data não pôde ser convertida
            df_cid_detalhes['MES_CMPT'] = df_cid_detalhes['MES_CMPT'].astype(int)


            if not df_cid_detalhes.empty:
                evolucao_mensal = df_cid_detalhes.groupby('MES_CMPT').agg(
                    internacoes_unicas=('N_AIH', 'nunique'),
                    custo_medio=('VAL_TOT', 'mean')
                ).reset_index()

                if not evolucao_mensal.empty:
                    fig_ts = px.line(
                        evolucao_mensal,
                        x='MES_CMPT',
                        y='internacoes_unicas',
                        title=f'Internações Únicas Mensais ({cid_selecionado}, {ano_selecionado})',
                        labels={'MES_CMPT': 'Mês', 'internacoes_unicas': 'Internações Únicas'},
                        markers=True
                    )
                    fig_ts.update_layout(xaxis=dict(tickmode='linear', dtick=1)) # Garante que todos os meses sejam mostrados
                    st.plotly_chart(fig_ts, use_container_width=True)

                    fig_ts_custo = px.line(
                        evolucao_mensal,
                        x='MES_CMPT',
                        y='custo_medio',
                        title=f'Custo Médio Mensal por Internação ({cid_selecionado}, {ano_selecionado})',
                        labels={'MES_CMPT': 'Mês', 'custo_medio': 'Custo Médio (R$)'},
                        markers=True
                    )
                    fig_ts_custo.update_layout(xaxis=dict(tickmode='linear', dtick=1))
                    st.plotly_chart(fig_ts_custo, use_container_width=True)

                else:
                    st.info(f"Não há dados mensais suficientes para gerar gráficos de evolução para {cid_selecionado} em {ano_selecionado}.")
            else:
                 st.info(f"Não foi possível extrair informações mensais para {cid_selecionado} em {ano_selecionado} (verifique formato da coluna DT_INTER).")

        else:
             st.warning(f"Não há dados detalhados para o diagnóstico {cid_selecionado} no ano {ano_selecionado}.")

    else:
        st.warning("Não há diagnósticos no Top N para exibir detalhes.")

# Nota: Certifique-se de que a coluna 'DT_INTER' exista na tabela 'fato'
# e esteja em um formato que o pandas possa converter para datetime (ex: YYYY-MM-DD)
# para que o gráfico de série temporal funcione corretamente.
# Se 'DT_INTER' não existir ou não for necessária para a análise mensal,
# remova a seção do gráfico de série temporal.