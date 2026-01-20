import pandas as pd
import sqlalchemy as sa

import conectandoBancoDeDados as cbd

# Conectando ao banco
nomeBanco = 'cid10'
senha = 'dan313852*'
host = 'localhost'
port = '5432'
nomeTabela = 'tabelamatrizcheia'

connTabelaCheia = cbd.conecting_database(nomeBanco, senha, host, port, nomeTabela)

# Pegando a tabela conectada e transformando em um dataframe
dfTabelaCheia = pd.read_sql_table(nomeTabela, connTabelaCheia)

connTabelaCid10 = cbd.conecting_database(nomeBanco, senha, host, port, 'cid10')
connTabelaCidSepse = cbd.conecting_database(nomeBanco, senha, host, port, 'cid10_sepse')
connTabelaCidInfeccaoTratoUrinario = cbd.conecting_database(nomeBanco, senha, host, port, 'cid10_infeccaotratourinario')
connTabelaCidPneumoniasBacterianas = cbd.conecting_database(nomeBanco, senha, host, port, 'cid10_pneumoniasbacterianas')

dfTabelaCid10 = pd.read_sql_table('cid10', connTabelaCid10)
dfTabelaCidSepse = pd.read_sql_table('cid10_sepse', connTabelaCidSepse)
dfTabelaCidInfeccaoTratoUrinario = pd.read_sql_table('cid10_infeccaotratourinario', connTabelaCidInfeccaoTratoUrinario)

# Filtrando os dados com os cids de sepse, infecção do trato urinário e pneumonias bacterianas