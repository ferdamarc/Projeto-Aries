import pandas as pd
import numpy as np
from datetime import datetime
import re
import os


def clean_dataframe(df):
    df_clean = df.copy()
    
    df_clean = df_clean.replace('', np.nan)
    df_clean = df_clean.replace(' ', np.nan)
    
    for col in df_clean.select_dtypes(include=['object']).columns:
        df_clean[col] = df_clean[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    date_columns = ['DT_INTER', 'DT_SAIDA', 'NASC', 'GESTOR_DT']
    for col in date_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], format='%Y%m%d', errors='coerce')
    
    numeric_columns = ['VAL_SH', 'VAL_SP', 'VAL_SADT', 'VAL_RN', 'VAL_ACOMP', 
                      'VAL_ORTP', 'VAL_SANGUE', 'VAL_SADTSR', 'VAL_TRANSP', 
                      'VAL_OBSANG', 'VAL_PED1AC', 'VAL_TOT', 'VAL_UTI', 
                      'US_TOT', 'VAL_SH_FED', 'VAL_SP_FED', 'VAL_SH_GES', 
                      'VAL_SP_GES', 'VAL_UCI']
    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col].astype(str).str.replace(',', '.'), errors='coerce')
    
    code_columns = ['DIAG_PRINC', 'DIAG_SECUN', 'CID_ASSO', 'CID_MORTE', 
                   'DIAGSEC1', 'DIAGSEC2', 'DIAGSEC3', 'DIAGSEC4', 
                   'DIAGSEC5', 'DIAGSEC6', 'DIAGSEC7', 'DIAGSEC8', 'DIAGSEC9',
                   'PROC_SOLIC', 'PROC_REA']
    for col in code_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace('nan', np.nan)
    
    return df_clean


def standardize_cid_codes(df):
    cid_columns = ['DIAG_PRINC', 'DIAG_SECUN', 'CID_ASSO', 'CID_MORTE', 
                  'DIAGSEC1', 'DIAGSEC2', 'DIAGSEC3', 'DIAGSEC4', 
                  'DIAGSEC5', 'DIAGSEC6', 'DIAGSEC7', 'DIAGSEC8', 'DIAGSEC9']
    
    for col in cid_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: re.sub(r'\s+', '', str(x)) if not pd.isna(x) else x)
            
            if col == 'DIAG_PRINC':
                df['GRUPO_DIAG_PRINC'] = df[col].apply(
                    lambda x: x[0] if isinstance(x, str) and len(x) > 0 and x[0].isalpha() else np.nan
                )
            
            if col == 'DIAG_PRINC':
                df['SUBGRUPO_DIAG_PRINC'] = df[col].apply(
                    lambda x: x[:3] if isinstance(x, str) and len(x) >= 3 else np.nan
                )
    
    proc_columns = ['PROC_SOLIC', 'PROC_REA']
    for col in proc_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: re.sub(r'\s+', '', str(x)) if not pd.isna(x) else x)
            
            if col == 'PROC_REA':
                df['GRUPO_PROC'] = df[col].apply(
                    lambda x: x[:2] if isinstance(x, str) and len(x) >= 2 and x.isdigit() else np.nan
                )
    
    return df


def generate_dimension_keys(df):
    df['ID_TEMPO'] = df.apply(
        lambda row: f"{row['ANO_CMPT']}{row['MES_CMPT']:02d}" 
        if not pd.isna(row['ANO_CMPT']) and not pd.isna(row['MES_CMPT']) 
        else np.nan, 
        axis=1
    )
    
    df['DIAS_PERMANENCIA'] = (df['DT_SAIDA'] - df['DT_INTER']).dt.days
    df.loc[df['DIAS_PERMANENCIA'] < 0, 'DIAS_PERMANENCIA'] = np.nan
    
    age_bins = [-1, 1, 4, 11, 17, 29, 59, 79, 200]
    age_labels = ['< 1 ano', '1-4 anos', '5-11 anos', '12-17 anos', '18-29 anos', '30-59 anos', '60-79 anos', '80+ anos']
    df['FAIXA_ETARIA'] = pd.cut(df['IDADE'], bins=age_bins, labels=age_labels)
    
    df['ID_PACIENTE'] = df.apply(lambda row: f"P{row.name}", axis=1)
    df['ID_HOSPITAL'] = df.apply(lambda row: f"H{row['CNES']}" if not pd.isna(row['CNES']) else np.nan, axis=1)
    df['ID_LOCALIZACAO'] = df.apply(lambda row: f"L{row['MUNIC_RES']}" if not pd.isna(row['MUNIC_RES']) else np.nan, axis=1)
    df['ID_PROCEDIMENTO'] = df.apply(lambda row: f"PR{row['PROC_REA']}" if not pd.isna(row['PROC_REA']) else np.nan, axis=1)
    df['ID_DIAGNOSTICO'] = df.apply(lambda row: f"D{row['DIAG_PRINC']}" if not pd.isna(row['DIAG_PRINC']) else np.nan, axis=1)
    
    df['UF_RES'] = df['MUNIC_RES'].astype(str).str[:2]
    df['UF_MOV'] = df['MUNIC_MOV'].astype(str).str[:2]
    
    return df


def transform_sih_specific_data(df):
    binary_columns = ['MORTE', 'MARCA_UTI', 'MARCA_UCI', 'INFEHOSP']
    for col in binary_columns:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: 1 if not pd.isna(x) and str(x).strip() in ['1', 'S', 'sim', 'SIM'] 
                else 0 if not pd.isna(x) else np.nan
            )
    
    if 'SEXO' in df.columns:
        sexo_map = {'1': 'Masculino', '3': 'Feminino', '0': 'Não informado'}
        df['DESC_SEXO'] = df['SEXO'].astype(str).map(sexo_map)
    
    if 'RACA_COR' in df.columns:
        raca_map = {
            '1': 'Branca',
            '2': 'Preta',
            '3': 'Parda',
            '4': 'Amarela',
            '5': 'Indígena',
            '99': 'Sem informação'
        }
        df['DESC_RACA_COR'] = df['RACA_COR'].astype(str).map(raca_map)
    
    if 'NASC' in df.columns and 'DT_INTER' in df.columns:
        df['IDADE_CALCULADA'] = (df['DT_INTER'] - df['NASC']).dt.days / 365.25
    
    if 'VAL_TOT' in df.columns and 'DIAS_PERMANENCIA' in df.columns:
        df['VAL_MEDIO_DIA'] = df.apply(
            lambda row: row['VAL_TOT'] / row['DIAS_PERMANENCIA'] 
            if not pd.isna(row['DIAS_PERMANENCIA']) and row['DIAS_PERMANENCIA'] > 0 
            else np.nan, 
            axis=1
        )
    
    if 'VAL_UTI' in df.columns:
        df['PASSOU_UTI'] = df['VAL_UTI'].apply(lambda x: 1 if x > 0 else 0)
    
    return df
    
def export_cleaned_data(df, output_path='dados_limpos'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    df.to_csv(os.path.join(output_path, 'sih_dados_limpos.csv'), sep=';', index=False)
    
    tempo_cols = ['ID_TEMPO', 'ANO_CMPT', 'MES_CMPT']
    df_tempo = df[tempo_cols].drop_duplicates()
    df_tempo.to_csv(os.path.join(output_path, 'dim_tempo.csv'), sep=';', index=False)
    
    paciente_cols = ['ID_PACIENTE', 'SEXO', 'DESC_SEXO', 'IDADE', 'FAIXA_ETARIA', 
                    'COD_IDADE', 'RACA_COR', 'DESC_RACA_COR', 'NACIONAL']
    df_paciente = df[paciente_cols].drop_duplicates()
    df_paciente.to_csv(os.path.join(output_path, 'dim_paciente.csv'), sep=';', index=False)
    
    hospital_cols = ['ID_HOSPITAL', 'CNES', 'CGC_HOSP']
    df_hospital = df[hospital_cols].drop_duplicates()
    df_hospital.to_csv(os.path.join(output_path, 'dim_hospital.csv'), sep=';', index=False)
    
    localizacao_cols = ['ID_LOCALIZACAO', 'MUNIC_RES', 'UF_RES', 'MUNIC_MOV', 'UF_MOV', 'CEP']
    df_localizacao = df[localizacao_cols].drop_duplicates()
    df_localizacao.to_csv(os.path.join(output_path, 'dim_localizacao.csv'), sep=';', index=False)
    
    procedimento_cols = ['ID_PROCEDIMENTO', 'PROC_REA', 'PROC_SOLIC', 'GRUPO_PROC']
    df_procedimento = df[procedimento_cols].drop_duplicates()
    df_procedimento.to_csv(os.path.join(output_path, 'dim_procedimento.csv'), sep=';', index=False)
    
    diagnostico_cols = ['ID_DIAGNOSTICO', 'DIAG_PRINC', 'GRUPO_DIAG_PRINC', 'SUBGRUPO_DIAG_PRINC',
                       'DIAG_SECUN', 'DIAGSEC1', 'DIAGSEC2', 'DIAGSEC3', 
                       'DIAGSEC4', 'DIAGSEC5', 'DIAGSEC6', 'DIAGSEC7', 
                       'DIAGSEC8', 'DIAGSEC9', 'CID_MORTE', 'CID_ASSO']
    df_diagnostico = df[diagnostico_cols].drop_duplicates()
    df_diagnostico.to_csv(os.path.join(output_path, 'dim_diagnostico.csv'), sep=';', index=False)
    
    fact_cols = ['N_AIH', 'ID_TEMPO', 'ID_PACIENTE', 'ID_HOSPITAL', 'ID_LOCALIZACAO',
                'ID_PROCEDIMENTO', 'ID_DIAGNOSTICO', 'DT_INTER', 'DT_SAIDA', 
                'MORTE', 'VAL_SH', 'VAL_SP', 'VAL_TOT', 'VAL_UTI', 'PASSOU_UTI',
                'DIAS_PERMANENCIA', 'VAL_MEDIO_DIA']
    df_fato = df[fact_cols]
    df_fato.to_csv(os.path.join(output_path, 'fato_internacao.csv'), sep=';', index=False)


def main():
    
    var_interesse = [
                    'ANO_CMPT', 'MES_CMPT', 'DT_INTER', 'DT_SAIDA', 'CEP', 'MUNIC_RES', 'MUNIC_MOV', 
                    'CGC_HOSP', 'CNES', 'NASC', 'SEXO', 'IDADE', 'COD_IDADE', 'NACIONAL', 'INSTRU', 
                    'RACA_COR', 'ETNIA', 'CBOR', 'MORTE', 'UTI_MES_TO', 'MARCA_UTI', 'VAL_UTI', 
                    'PROC_SOLIC', 'PROC_REA', 'VAL_SH', 'VAL_SP', 'N_AIH', 'VAL_TOT', 'INFEHOSP',
                    'DIAG_PRINC', 'DIAG_SECUN', 'DIAGSEC1', 'DIAGSEC2', 'DIAGSEC3', 'DIAGSEC4', 
                    'DIAGSEC5', 'DIAGSEC6', 'DIAGSEC7', 'DIAGSEC8', 'DIAGSEC9', 'CID_MORTE', 'CID_ASSO'
                ]
    
    # Definir arquivo de entrada e testar o dashboard com esse novo df
    file_path = r'C:\Users\Fernando\Documents\CEPID - Projeto ARIES\Aries-Project\data\brutos\SIH\csv\2023\RDSP2302.csv'    
    output_path = r'c:\Users\Fernando\Documents\CEPID - Projeto ARIES\Aries-Project\data\processados\SIH\Teste'
    
    df = pd.read_csv(
        file_path,
        sep=';',
        encoding='latin1',
        low_memory=False,
        usecols=var_interesse,
        nrows=5000,
    )
    
    df_clean = clean_dataframe(df)
    df_clean = standardize_cid_codes(df_clean)
    df_dimensional = generate_dimension_keys(df_clean)
    df_transformed = transform_sih_specific_data(df_dimensional)
    export_cleaned_data(df_transformed, output_path)


if __name__ == "__main__":
    main()