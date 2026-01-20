from pysus.ftp.databases.sih import SIH
import pandas as pd

def downloadDadosSIHSUSparquet(grupo, uf, ano, mes, path):
    sih = SIH().load()
    
    files = sih.get_files(grupo, uf, ano, mes)
        
    downloads = sih.download(files, local_dir=path)
    
    return downloads

def downloadDadosSIHSUScsv(downloadParquet, path):
    dfs = []
    
    for parquet in downloadParquet:
        df = pd.read_parquet(parquet)
        dfs.append(df)
        
    for df in dfs:
        df.to_csv(f'{path}/{df}.csv', sep=';', encoding = 'ISO-8859-1', index=False)
        
    return dfs
