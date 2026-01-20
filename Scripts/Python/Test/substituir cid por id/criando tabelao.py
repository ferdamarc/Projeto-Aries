import pandas as pd
import sqlalchemy as sa

import sys
sys.path.append(r'C:\Users\Fernando\Documents\CEPID - Projeto ARIES\Scripts\Python\Test')
import conectandoBancoDeDados as cbd

class tabela_cheia:
    def __init__(self, namebd):
        self.nome_tabela = namebd
        
        self.colunas = ['ANO_CMPT', 'MES_CMPT', 'DT_INTER', 'DT_SAIDA', 'CEP', 'MUNIC_RES', 'MUNIC_MOV', 
                        'CGC_HOSP', 'CNES', 'NASC', 'SEXO', 'IDADE', 'COD_IDADE', 'NACIONAL', 'INSTRU', 
                        'RACA_COR', 'ETNIA', 'CBOR', 'MORTE', 'UTI_MES_TO', 'MARCA_UTI', 'VAL_UTI', 
                        'PROC_SOLIC', 'PROC_REA', 'VAL_SH', 'VAL_SP', 'N_AIH', 'VAL_TOT', 'INFEHOSP',
                        'DIAG_PRINC', 'DIAG_SECUN', 'DIAGSEC1', 'DIAGSEC2', 'DIAGSEC3', 'DIAGSEC4', 
                        'DIAGSEC5', 'DIAGSEC6', 'DIAGSEC7', 'DIAGSEC8', 'DIAGSEC9', 'CID_MORTE', 'CID_ASSO']
        
    def __str__(self):
        return f'Tabela {self.nome_tabela}'
    
    def cria_tabela(self, conn):
        metadata = sa.MetaData()
        metadata.reflect(bind=conn)
        
        if self.nome_tabela in metadata.tables:
            print(f'Tabela {self.nome_tabela} já existe.')
            return
        
        sa.Table(self.nome_tabela, sa.MetaData(),
                sa.Column('ANO_CMPT', sa.VARCHAR(4)),
                sa.Column('MES_CMPT', sa.VARCHAR(2)),
                sa.Column('DT_INTER', sa.VARCHAR(8)),
                sa.Column('DT_SAIDA', sa.VARCHAR(8)),
                sa.Column('CEP', sa.VARCHAR(8)),
                sa.Column('MUNIC_RES', sa.VARCHAR(6)),
                sa.Column('MUNIC_MOV', sa.VARCHAR(6)),
                sa.Column('CGC_HOSP', sa.VARCHAR(16)),
                sa.Column('CNES', sa.VARCHAR(7)),
                sa.Column('NASC', sa.VARCHAR(8)),
                sa.Column('SEXO', sa.VARCHAR(1)),
                sa.Column('IDADE', sa.NUMERIC(2)),
                sa.Column('COD_IDADE', sa.VARCHAR(1)),
                sa.Column('NACIONAL', sa.VARCHAR(3)),
                sa.Column('INSTRU', sa.VARCHAR(1)),
                sa.Column('RACA_COR', sa.VARCHAR(2)),
                sa.Column('ETNIA', sa.VARCHAR(4)),
                sa.Column('CBOR', sa.VARCHAR(6)),
                sa.Column('MORTE', sa.NUMERIC(1)),
                sa.Column('UTI_MES_TO', sa.NUMERIC(3)),
                sa.Column('MARCA_UTI', sa.VARCHAR(2)),
                sa.Column('VAL_UTI', sa.NUMERIC(9,2)),
                sa.Column('PROC_SOLIC', sa.VARCHAR(10)),
                sa.Column('PROC_REA', sa.VARCHAR(10)),
                sa.Column('VAL_SH', sa.NUMERIC(13,2)),
                sa.Column('VAL_SP', sa.NUMERIC(13,2)),
                sa.Column('N_AIH', sa.VARCHAR(13)),
                sa.Column('VAL_TOT', sa.NUMERIC(14,2)),
                sa.Column('INFEHOSP', sa.VARCHAR(1)),
                sa.Column('DIAG_PRINC', sa.VARCHAR(4)),
                sa.Column('DIAG_SECUN', sa.VARCHAR(4)),
                sa.Column('DIAGSEC1', sa.VARCHAR(4)),
                sa.Column('DIAGSEC2', sa.VARCHAR(4)),
                sa.Column('DIAGSEC3', sa.VARCHAR(4)),
                sa.Column('DIAGSEC4', sa.VARCHAR(4)),
                sa.Column('DIAGSEC5', sa.VARCHAR(4)),
                sa.Column('DIAGSEC6', sa.VARCHAR(4)),
                sa.Column('DIAGSEC7', sa.VARCHAR(4)),
                sa.Column('DIAGSEC8', sa.VARCHAR(4)),
                sa.Column('DIAGSEC9', sa.VARCHAR(4)),
                sa.Column('CID_MORTE', sa.VARCHAR(4)),
                sa.Column('CID_ASSO', sa.VARCHAR(4))
        ).create(conn)
        
    def insere_dados(self, df, conn):
        df.to_sql(self.nome_tabela, conn, if_exists='append', index=False, dtype={
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
            'CID_ASSO': sa.VARCHAR(4)}
        )
        
    def remove_tabela(self, conn):
        metadata = sa.MetaData()
        metadata.reflect(bind=conn)
        
        if self.nome_tabela not in metadata.tables:
            print(f'Tabela {self.nome_tabela} não existe.')
            return
        
        sa.Table(self.nome_tabela, sa.MetaData(),
                sa.Column('ANO_CMPT', sa.VARCHAR(4)),
                sa.Column('MES_CMPT', sa.VARCHAR(2)),
                sa.Column('DT_INTER', sa.VARCHAR(8)),
                sa.Column('DT_SAIDA', sa.VARCHAR(8)),
                sa.Column('CEP', sa.VARCHAR(8)),
                sa.Column('MUNIC_RES', sa.VARCHAR(6)),
                sa.Column('MUNIC_MOV', sa.VARCHAR(6)),
                sa.Column('CGC_HOSP', sa.VARCHAR(16)),
                sa.Column('CNES', sa.VARCHAR(7)),
                sa.Column('NASC', sa.VARCHAR(8)),
                sa.Column('SEXO', sa.VARCHAR(1)),
                sa.Column('IDADE', sa.NUMERIC(2)),
                sa.Column('COD_IDADE', sa.VARCHAR(1)),
                sa.Column('NACIONAL', sa.VARCHAR(3)),
                sa.Column('INSTRU', sa.VARCHAR(1)),
                sa.Column('RACA_COR', sa.VARCHAR(2)),
                sa.Column('ETNIA', sa.VARCHAR(4)),
                sa.Column('CBOR', sa.VARCHAR(6)),
                sa.Column('MORTE', sa.NUMERIC(1)),
                sa.Column('UTI_MES_TO', sa.NUMERIC(3)),
                sa.Column('MARCA_UTI', sa.VARCHAR(2)),
                sa.Column('VAL_UTI', sa.NUMERIC(9,2)),
                sa.Column('PROC_SOLIC', sa.VARCHAR(10)),
                sa.Column('PROC_REA', sa.VARCHAR(10)),
                sa.Column('VAL_SH', sa.NUMERIC(13,2)),
                sa.Column('VAL_SP', sa.NUMERIC(13,2)),
                sa.Column('N_AIH', sa.VARCHAR(13)),
                sa.Column('VAL_TOT', sa.NUMERIC(14,2)),
                sa.Column('INFEHOSP', sa.VARCHAR(1)),
                sa.Column('DIAG_PRINC', sa.VARCHAR(4)),
                sa.Column('DIAG_SECUN', sa.VARCHAR(4)),
                sa.Column('DIAGSEC1', sa.VARCHAR(4)),
                sa.Column('DIAGSEC2', sa.VARCHAR(4)),
                sa.Column('DIAGSEC3', sa.VARCHAR(4)),
                sa.Column('DIAGSEC4', sa.VARCHAR(4)),
                sa.Column('DIAGSEC5', sa.VARCHAR(4)),
                sa.Column('DIAGSEC6', sa.VARCHAR(4)),
                sa.Column('DIAGSEC7', sa.VARCHAR(4)),
                sa.Column('DIAGSEC8', sa.VARCHAR(4)),
                sa.Column('DIAGSEC9', sa.VARCHAR(4)),
                sa.Column('CID_MORTE', sa.VARCHAR(4)),
                sa.Column('CID_ASSO', sa.VARCHAR(4))
        ).drop(conn)
        
# Importando os dados e criando um dataframe        
pathData = r'C:\Users\Fernando\Documents\CEPID - Projeto ARIES\data\brutos\SIH\csv\concat\concat_RDSP02_filtered.csv'
df = pd.read_csv(pathData, sep=';', encoding='latin1')

# Conectando ao banco
import conectandoBancoDeDados as cbd
user = 'postgres'
senha = 'dan313852*'
host = 'localhost'
port = '5432'
nomeBanco = 'cid-10'
nomeTabela = 'tabelacheiamatriz'

conn = cbd.conecting_database(user, senha, host, port, nomeBanco)

# Criando a tabela
tabela = tabela_cheia(nomeTabela)
tabela.cria_tabela(conn)

# Inserindo os dados
tabela.insere_dados(df, conn)

# Desconectando do banco
cbd.desconecting_database(conn)