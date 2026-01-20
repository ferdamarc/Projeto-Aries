from dbfread import DBF

# Caminho para o arquivo DBF
file_path = r"C:\Users\Fernando\Documents\CEPID - Projeto ARIES\data\informacoes\sim\TABELAS-CID10\CID10.DBF"

# Carregar o arquivo e exibir os campos
table = DBF(file_path, encoding='latin-1')  # Ajuste o encoding se necessário
print("Colunas do arquivo DBF:")

records = list(table)  # Convert the iterator to a list

for field in table.field_names:
    print(field + ": " + type(records[0][field]).__name__)
    print("\nNome da coluna, tipo e tamanho:")
    for field in table.fields:
        print(f"Nome: {field.name}, Tipo: {field.type}, Tamanho: {field.length}")