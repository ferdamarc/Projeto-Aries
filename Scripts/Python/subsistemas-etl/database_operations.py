import sqlalchemy as sa
import pandas as pd
from datetime import datetime
import numpy as np

class tabela_cheia:
    
    def __init__(self):
        
        self.colunas = ['ANO_CMPT', 'MES_CMPT', 'DT_INTER', 'DT_SAIDA', 'CEP', 'MUNIC_RES', 'MUNIC_MOV', 
                        'CGC_HOSP', 'CNES', 'NASC', 'SEXO', 'IDADE', 'COD_IDADE', 'NACIONAL', 'INSTRU', 
                        'RACA_COR', 'ETNIA', 'CBOR', 'MORTE', 'UTI_MES_TO', 'MARCA_UTI', 'VAL_UTI', 
                        'PROC_SOLIC', 'PROC_REA', 'VAL_SH', 'VAL_SP', 'N_AIH', 'VAL_TOT', 'INFEHOSP',
                        'DIAG_PRINC', 'DIAG_SECUN', 'DIAGSEC1', 'DIAGSEC2', 'DIAGSEC3', 'DIAGSEC4', 
                        'DIAGSEC5', 'DIAGSEC6', 'DIAGSEC7', 'DIAGSEC8', 'DIAGSEC9', 'CID_MORTE', 'CID_ASSO']
        
        # Definicao dos tipos de dados padrao para as colunas
        self._tipos_dados = {
            'ANO_CMPT': sa.VARCHAR(4),
            'MES_CMPT': sa.VARCHAR(2),
            'DT_INTER': sa.VARCHAR(8),
            'DT_SAIDA': sa.VARCHAR(8),
            'CEP': sa.VARCHAR(8),
            'MUNIC_RES': sa.VARCHAR(6),
            'MUNIC_MOV': sa.VARCHAR(6),
            'CGC_HOSP': sa.VARCHAR(16),
            'CNES': sa.VARCHAR(7),
            'NASC': sa.VARCHAR(8),
            'SEXO': sa.VARCHAR(1),
            'IDADE': sa.NUMERIC(2),
            'COD_IDADE': sa.VARCHAR(1),
            'NACIONAL': sa.VARCHAR(3),
            'INSTRU': sa.VARCHAR(1),
            'RACA_COR': sa.VARCHAR(2),
            'ETNIA': sa.VARCHAR(4),
            'CBOR': sa.VARCHAR(6),
            'MORTE': sa.NUMERIC(1),
            'UTI_MES_TO': sa.NUMERIC(3),
            'MARCA_UTI': sa.VARCHAR(2),
            'VAL_UTI': sa.NUMERIC(9,2),
            'PROC_SOLIC': sa.VARCHAR(10),
            'PROC_REA': sa.VARCHAR(10),
            'VAL_SH': sa.NUMERIC(13,2),
            'VAL_SP': sa.NUMERIC(13,2),
            'N_AIH': sa.VARCHAR(13),
            'VAL_TOT': sa.NUMERIC(14,2),
            'INFEHOSP': sa.VARCHAR(1),
            'DIAG_PRINC': sa.VARCHAR(4),
            'DIAG_SECUN': sa.VARCHAR(4),
            'DIAGSEC1': sa.VARCHAR(4),
            'DIAGSEC2': sa.VARCHAR(4),
            'DIAGSEC3': sa.VARCHAR(4),
            'DIAGSEC4': sa.VARCHAR(4),
            'DIAGSEC5': sa.VARCHAR(4),
            'DIAGSEC6': sa.VARCHAR(4),
            'DIAGSEC7': sa.VARCHAR(4),
            'DIAGSEC8': sa.VARCHAR(4),
            'DIAGSEC9': sa.VARCHAR(4),
            'CID_MORTE': sa.VARCHAR(4),
            'CID_ASSO': sa.VARCHAR(4)
        }
        
        # Definicao dos tipos de dados padrao para as colunas caso eu queira mudar a forma de inserir no banco
        self._tipos_dados_filtrados = {
            'ANO_CMPT': sa.VARCHAR(4),
            'MES_CMPT': sa.VARCHAR(2),
            'DT_INTER': sa.VARCHAR(8),
            'DT_SAIDA': sa.VARCHAR(8),
            'CEP': sa.VARCHAR(8),
            'MUNIC_RES': sa.VARCHAR(6),
            'MUNIC_MOV': sa.VARCHAR(6),
            'CGC_HOSP': sa.VARCHAR(16),
            'CNES': sa.VARCHAR(7),
            'NASC': sa.VARCHAR(8),
            'SEXO': sa.VARCHAR(1),
            'IDADE': sa.NUMERIC(2),
            'COD_IDADE': sa.VARCHAR(1),
            'NACIONAL': sa.VARCHAR(3),
            'INSTRU': sa.VARCHAR(1),
            'RACA_COR': sa.VARCHAR(2),
            'ETNIA': sa.VARCHAR(4),
            'CBOR': sa.VARCHAR(6),
            'MORTE': sa.NUMERIC(1),
            'UTI_MES_TO': sa.NUMERIC(3),
            'MARCA_UTI': sa.VARCHAR(2),
            'VAL_UTI': sa.NUMERIC(9,2),
            'PROC_SOLIC': sa.VARCHAR(10),
            'PROC_REA': sa.VARCHAR(10),
            'VAL_SH': sa.NUMERIC(13,2),
            'VAL_SP': sa.NUMERIC(13,2),
            'N_AIH': sa.VARCHAR(13),
            'VAL_TOT': sa.NUMERIC(14,2),
            'INFEHOSP': sa.VARCHAR(1),
            'DIAG_PRINC': sa.VARCHAR(4),
            'DIAG_SECUN': sa.VARCHAR(4),
            'DIAGSEC1': sa.VARCHAR(4),
            'DIAGSEC2': sa.VARCHAR(4),
            'DIAGSEC3': sa.VARCHAR(4),
            'DIAGSEC4': sa.VARCHAR(4),
            'DIAGSEC5': sa.VARCHAR(4),
            'DIAGSEC6': sa.VARCHAR(4),
            'DIAGSEC7': sa.VARCHAR(4),
            'DIAGSEC8': sa.VARCHAR(4),
            'DIAGSEC9': sa.VARCHAR(4),
            'CID_MORTE': sa.VARCHAR(4),
            'CID_ASSO': sa.VARCHAR(4)
        }
        
    def nome_tabela(self, nome_tabela):
        self.nome_tabela = nome_tabela
        
    '''
    O @property é um decorador em Python que permite que um método de classe seja acessado 
    como se fosse um atributo, sem necessidade de usar parênteses para chamá-lo.
    '''
    @property
    def tipos_dados(self):
        return self._tipos_dados
    
    @property
    def tipos_dados_filtrados(self):
        return self._tipos_dados_filtrados
    
    def cria_tabela(self, conn):
        metadata = sa.MetaData()
        metadata.reflect(bind=conn)
        
        if self.nome_tabela in metadata.tables:
            print(f'Tabela {self.nome_tabela} ja existe.')
            return
        
        # Criando uma tabela usando os tipos definidos no dicionário self._tipos_dados
        tabela = sa.Table(self.nome_tabela, sa.MetaData())
        
        # Adiciona colunas à tabela
        for coluna, tipo in self._tipos_dados.items():
            tabela.append_column(sa.Column(coluna, tipo))
        
        # Cria a tabela no banco
        tabela.create(conn)
        print(f'Tabela {self.nome_tabela} criada com sucesso.')
        
    def insere_dados(self, df, conn, if_exists='append', chunksize=None):
        df.to_sql(self.nome_tabela, conn, if_exists=if_exists, index=False, 
                 dtype=self._tipos_dados, chunksize=chunksize)
        
        if chunksize:
            print(f'Dados inseridos com sucesso na tabela {self.nome_tabela} em lotes de {chunksize} registros.')
        else:
            print(f'Dados inseridos com sucesso na tabela {self.nome_tabela}.')
            
    def insere_dados_filtrados(self, df, conn, if_exists='append', chunksize=None):
        df.to_sql(self.nome_tabela, conn, if_exists=if_exists, index=False, dtype=self._tipos_dados_filtrados, chunksize=chunksize)
        
        if chunksize:
            print(f'Dados filtrados inseridos com sucesso na tabela {self.nome_tabela} em lotes de {chunksize} registros.')
        else:
            print(f'Dados filtrados inseridos com sucesso na tabela {self.nome_tabela}.')
        
    def remove_tabela(self, conn, nome_tabela=None):
        tabela_alvo = nome_tabela or self.nome_tabela
        
        metadata = sa.MetaData()
        metadata.reflect(bind=conn)
        
        if tabela_alvo not in metadata.tables:
            print(f'Tabela {tabela_alvo} nao existe.')
            return
        
        # Obtem a tabela do metadata e remove
        metadata.tables[tabela_alvo].drop(conn)
        print(f'Tabela {tabela_alvo} removida com sucesso.')


# Funcao auxiliar para converter datas (formato DDMMAAAA para AAAA-MM-DD)
# Ainda não utilizei, mas pensei eu fazer isso
def convert_date(date_str):
    if pd.isna(date_str) or date_str == '':
        return pd.NaT
    
    try:
        return datetime.strptime(str(date_str), '%Y%m%d').date()
    except Exception as e:
        return pd.NaT


def transform_data(df):
    
    df_trans = df.copy()
    
    return df_trans
