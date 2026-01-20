import pandas as pd
import psycopg2

def tamanho_maximo_colunas(df):
    """
    Percorre todas as colunas de um DataFrame e calcula o tamanho máximo de cada coluna.

    Args:
        df (pd.DataFrame): O DataFrame a ser analisado.

    Returns:
        dict: Um dicionário com os nomes das colunas e seus respectivos tamanhos máximos.
    """
    resultado = {}
    for coluna in df.columns:
        # Calcular o tamanho máximo da coluna (número de caracteres)
        max_tamanho = df[coluna].astype(str).map(len).max()
        resultado[coluna] = max_tamanho
    
    return resultado

# Configurações do banco de dados
db_config = {
    'dbname': 'cid-10',           # Nome do banco
    'user': 'postgres',           # Usuário do PostgreSQL
    'password': 'dan313852*',         # Senha do PostgreSQL
    'host': 'localhost',             # Host do banco
    'port': 5432                     # Porta padrão do PostgreSQL
}

# Caminho do arquivo CSV
csv_file_path = r"C:\Users\Fernando\Documents\CEPID - Projeto ARIES\data\informacoes\sim\TABELAS-CID10\CID10.csv"

# Ler o CSV com pandas
df = pd.read_csv(csv_file_path)

# Mostrando o tamanho máximo de cada coluna
tamanhos = tamanho_maximo_colunas(df)
print(tamanhos)

# Conexão com o PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida.")

    # Loop para inserir os dados linha por linha
    for _, row in df.iterrows():
        query = """
        INSERT INTO cid10 (cid10, opc, cat, subcat, descr, restrsexo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            row['CID10'],  # Ajuste os nomes para corresponder às colunas do CSV
            row['OPC'],
            row['CAT'],
            row['SUBCAT'],
            row['DESCR'],
            row['RESTRSEXO']
        ))

    # Confirmar transação
    conn.commit()
    print("Dados importados com sucesso!")

except Exception as e:
    print("Erro ao conectar ou importar os dados:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("Conexão com o banco de dados fechada.")