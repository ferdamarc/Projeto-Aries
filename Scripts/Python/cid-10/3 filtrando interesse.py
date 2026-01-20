import pandas as pd
import psycopg2

# Vetor para CIDs relacionados à sepse
cid10_interesse_sepse = [
    "A021", "A039", "A207", "A217", "A227", "A239", "A241", "A267", "A280", "A282",
    "A327", "A392", "A393", "A394", "A40", "A400", "A401", "A402", "A403", "A408",
    "A409", "A41", "A410", "A411", "A412", "A413", "A414", "A415", "A418", "A419",
    "A427", "B007", "B377", "P352", "P36", "P360", "P361", "P362", "P363", "P364",
    "P365", "P368", "P369", "P372", "P375"
]

# Vetor para CIDs relacionados a pneumonias bacterianas
cid10_interesse_pneumonias_bacterianas = [
    "J13", "J14", "J150", "J151", "J152", "J153", "J154", "J155", "J156", "J157",
    "J158", "J159", "J16", "J160", "J168", "J170", "J178", "J180", "J181", "J182",
    "J188", "J189", "J851", "P231", "P232", "P233", "P234", "P235", "P236", "P238",
    "P239", "J860", "J869"
]

# Vetor para CIDs relacionados a infecções do trato urinário
cid10_interesse_infeccao_trato_urinario = [
    "N080", "N110", "N111", "N151", "N300", "N301", "N302", "N308", "N340", "N390",
    "O233", "O234", "O239", "O862", "O863", "P393"
]

# Configurações do banco de dados
db_config = {
    'dbname': 'cid-10',           # Nome do banco
    'user': 'postgres',           # Usuário do PostgreSQL
    'password': 'dan313852*',     # Senha do PostgreSQL
    'host': 'localhost',          # Host do banco
    'port': 5432                  # Porta padrão do PostgreSQL
}

def filtrar_dados(cursor, vetor_cids, descricao, output_file):
    cursor.execute("SELECT * FROM cid10 WHERE cid10 IN %s", (tuple(vetor_cids),))
    dados = cursor.fetchall()
    output_file.write(f"{descricao}:\n")
    for linha in dados:
        output_file.write(f"{linha}\n")
    output_file.write("\n")

# Conectando ao banco de dados
try:
    # Conexão com o PostgreSQL estabelecida
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida.")

    # Verificando se a tabela cid10 existe
    cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'cid10'")
    if not cursor.fetchone():
        print("Tabela cid10 não encontrada.")
        exit()

    # Abrindo o arquivo de saída
    with open(r"C:\Users\Fernando\Documents\CEPID - Projeto ARIES\Scripts\Python\cid-10\saida_filtrada.txt", "w") as output_file:
        # Filtrando os dados de interesse para sepse
        filtrar_dados(cursor, cid10_interesse_sepse, "Sepse", output_file)
        
        # Filtrando os dados de interesse para pneumonias bacterianas
        filtrar_dados(cursor, cid10_interesse_pneumonias_bacterianas, "Pneumonias bacterianas", output_file)
        
        # Filtrando os dados de interesse para infecções do trato urinário
        filtrar_dados(cursor, cid10_interesse_infeccao_trato_urinario, "Infecções do trato urinário", output_file)

    print("Dados filtrados com sucesso!")

except Exception as e:
    print("Erro ao conectar ou filtrar os dados:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
        print("Conexão com o banco de dados encerrada.")
