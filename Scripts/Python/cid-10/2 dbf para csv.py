import csv
from dbfread import DBF

# Caminho para o DBF e o CSV
dbf_path = r"C:\Users\Fernando\Documents\CEPID - Projeto ARIES\data\informacoes\sim\TABELAS-CID10\CID10.DBF"
csv_path = r"C:\Users\Fernando\Documents\CEPID - Projeto ARIES\data\informacoes\sim\TABELAS-CID10\CID10.csv"

# Converter DBF para CSV
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    table = DBF(dbf_path, encoding='latin-1')  # Ajuste o encoding conforme necessário
    
    # Escreve os nomes das colunas
    writer.writerow(table.field_names)
    
    # Escreve os dados
    for record in table:
        writer.writerow(record.values())
