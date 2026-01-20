import psycopg2

# Configurações do banco de dados
db_config = {
    'dbname': 'cid-10',           # Nome do banco
    'user': 'postgres',           # Usuário do PostgreSQL
    'password': 'dan313852*',     # Senha do PostgreSQL
    'host': 'localhost',          # Host do banco
    'port': 5432                  # Porta padrão do PostgreSQL
}

# Vetores com os CIDs de interesse
cid10_interesse_sepse = [
    "A021", "A039", "A207", "A217", "A227", "A239", "A241", "A267", "A280", "A282",
    "A327", "A392", "A393", "A394", "A40", "A400", "A401", "A402", "A403", "A408",
    "A409", "A41", "A410", "A411", "A412", "A413", "A414", "A415", "A418", "A419",
    "A427", "B007", "B377", "P352", "P36", "P360", "P361", "P362", "P363", "P364",
    "P365", "P368", "P369", "P372", "P375"
]

cid10_interesse_pneumonias_bacterianas = [
    "J13", "J14", "J150", "J151", "J152", "J153", "J154", "J155", "J156", "J157",
    "J158", "J159", "J16", "J160", "J168", "J170", "J178", "J180", "J181", "J182",
    "J188", "J189", "J851", "P231", "P232", "P233", "P234", "P235", "P236", "P238",
    "P239", "J860", "J869"
]

cid10_interesse_infeccao_trato_urinario = [
    "N080", "N110", "N111", "N151", "N300", "N301", "N302", "N308", "N340", "N390",
    "O233", "O234", "O239", "O862", "O863", "P393"
]

# Função para popular as tabelas
def popular_tabela(cursor, vetor_cids, tabela_destino):
    # Buscar todas as colunas para os CIDs especificados
    cursor.execute("SELECT * FROM cid10 WHERE cid10 IN %s", (tuple(vetor_cids),))
    dados = cursor.fetchall()
    
    if not dados:
        print(f"Nenhum CID encontrado para a tabela {tabela_destino}.")
        return

    # Inserir os dados na tabela de destino
    colunas = [desc[0] for desc in cursor.description]  # Pegar os nomes das colunas
    colunas_str = ', '.join(colunas)
    valores_placeholder = ', '.join(['%s'] * len(colunas))
    
    for registro in dados:
        cursor.execute(f"INSERT INTO {tabela_destino} ({colunas_str}) VALUES ({valores_placeholder})", registro)
    print(f"Tabela {tabela_destino} populada com {len(dados)} registros.")

# Conexão com o banco de dados
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida.")
    
    # Verificar se a tabela cid10 existe
    cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'cid10'")
    if not cursor.fetchone():
        print("Tabela cid10 não encontrada.")
        exit()
    
    # Popular as tabelas de destino
    popular_tabela(cursor, cid10_interesse_sepse, 'cid10_sepse')
    popular_tabela(cursor, cid10_interesse_pneumonias_bacterianas, 'cid10_pneumoniasbacterianas')
    popular_tabela(cursor, cid10_interesse_infeccao_trato_urinario, 'cid10_infeccaotratourinario')

    # Commitar as alterações
    conn.commit()
    print("Dados inseridos com sucesso.")

except Exception as e:
    print("Erro ao popular as tabelas:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
        print("Conexão com o banco de dados encerrada.")
