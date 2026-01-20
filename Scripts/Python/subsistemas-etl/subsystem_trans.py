#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime
from conectando_bd import conecting_database, desconecting_database
from database_operations import tabela_cheia, transform_data


def configurar_conexao():
    USER = "postgres"
    PASSWORD = "dan313852*"
    HOST = "localhost"
    PORT = "5432"
    DATABASE = "transform_test"
    
    engine = conecting_database(USER, PASSWORD, HOST, PORT, DATABASE)
    
    return engine


def ler_dados_amostra():
    data_path = r"C:\Users\Fernando\Documents\CEPID - Projeto ARIES\Aries-Project\data\brutos\SIH\csv\outros\bruto_20_amostras.csv"
    df_amostra = pd.read_csv(data_path, sep=",", encoding="UTF-8")
    
    return df_amostra


def inserir_dados_banco(engine, df_amostra):
    try:
        tabela_sihsus = tabela_cheia()
        tabela_sihsus.nome_tabela = "amostras_sihsus"
        tabela_sihsus.cria_tabela(engine)
        
        colunas_df = [col for col in df_amostra.columns if col in tabela_sihsus.colunas]
        df_para_inserir = df_amostra[colunas_df].copy()
        
        tabela_sihsus.insere_dados(df_para_inserir, engine)
        
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False


def ler_dados_banco(engine):
    try:
        query = "SELECT * FROM amostras_sihsus"
        df_lido = pd.read_sql(query, engine)
        
        print(f"Dados lidos com sucesso.")
        
        if len(df_lido) == 0:
            print("Sem dados")
        
        return df_lido
    except Exception as e:
        print(f"Erro: {e}")
        return None


def transformar_dados(df_lido):
    try:
        df_transformado = transform_data(df_lido)
        return df_transformado
    except Exception as e:
        print(f"Erro: {e}")
        return None


def inserir_dados_transformados(engine, df_transformado):
    try:
        tabela_transformada = tabela_cheia()
        tabela_transformada.nome_tabela = "amostras_sihsus_transformadas"
        
        tabela_transformada.cria_tabela(engine)
        tabela_transformada.insere_dados_filtrados(df_transformado, engine)
        
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False


def verificar_tabelas(engine):
    try:
        query_check = """
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name IN ('amostras_sihsus', 'amostras_sihsus_transformadas')
        """
        # tabelas_existentes = pd.read_sql(query_check, engine)
        
        # if not tabelas_existentes.empty:
        #     print(f"Tabelas: {', '.join(tabelas_existentes['table_name'].tolist())}")
            
        #     for tabela in tabelas_existentes['table_name']:
        #         query_count = f"SELECT COUNT(*) as total FROM {tabela}"
        #         count_result = pd.read_sql(query_count, engine)
        #         print(f"Registros em '{tabela}': {count_result['total'].iloc[0]}")
                
        #         query_cols = f"""
        #         SELECT column_name, data_type 
        #         FROM information_schema.columns
        #         WHERE table_schema = 'public' AND table_name = '{tabela}'
        #         ORDER BY ordinal_position
        #         """
        #         cols_result = pd.read_sql(query_cols, engine)
        #         print(f"Estrutura de '{tabela}':")
        #         print(cols_result)
        # else:
        #     print("Tabelas nao encontradas")
    except Exception as e:
        print(f"Erro: {e}")


def main():
    engine = configurar_conexao()
    if engine is None:
        return
    
    try:
        df_amostra = ler_dados_amostra()
        
        if not inserir_dados_banco(engine, df_amostra):
            print("Falha na insercao")
            return
        
        df_lido = ler_dados_banco(engine)
        if df_lido is None:
            print("Falha na leitura")
            return
        
        df_transformado = transformar_dados(df_lido)
        if df_transformado is None:
            print("Falha na transformacao")
            return
        
        if not inserir_dados_transformados(engine, df_transformado):
            print("Falha na insercao dos dados transformados")
            return
        
        verificar_tabelas(engine)
    
    except Exception as e:
        print(f"Erro: {e}")
    
    finally:
        if engine:
            desconecting_database(engine)
            print("ETL concluido")


if __name__ == "__main__":
    main()
