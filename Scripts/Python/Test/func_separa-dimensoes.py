from sqlalchemy import Numeric, CHAR
import pandas as pd

'''
Parei na parte de deixar o dicionario certo conforme o dicionário em csv.
Em seguida preciso fazer a separação das dimensões, mas acredito que isso já esteja feito.
'''

dimensoes = {
    'Dimensão temporal': {
        'tableNameInDataBase': 'dim_tempo',
        'columns': {
            'ANO_CMPT': {'type': CHAR(4), 'Description': 'Ano de processamento da AIH (Autorização de Internação Hospitalar)', 'Definition': 'AAAA'},
            'MES_CMPT': {'type': CHAR(2), 'Description': 'Mês de processamento da AIH (Autorização de Internação Hospitalar)', 'Definition': 'MM'},
            'DT_INTER':{'type': CHAR(8), 'Description': 'Data de internação', 'Definition': 'AAAAMMDD'},
            'DT_SAIDA':{'type': CHAR(8), 'Description': 'Data de saída', 'Definition': 'AAAAMMDD'},
        }
    },
    
    'Dimensão Localização': {
        'tableNameInDataBase': 'dim_localizacao',
        'columns': {
            'CEP': {'type': CHAR(8), 'Description': 'CEP do endereço do paciente', 'Definition': '########'},
            'MUNIC_RES': {'type': CHAR(6), 'Description': 'Código IBGE do município de residência do paciente', 'Definition': '######'},
            'MUNIC_MOV': {'type': CHAR(6), 'Description': 'Código do município onde se localiza o hospital', 'Definition': '######'},
        }
    },
    
    'Dimensão Hospital': {
        'tableNameInDataBase': 'dim_hospital',
        'columns': {
            'CGC_HOSP': {'type': CHAR(14), 'Description': 'CNPJ do estabelecimento de saúde (hospital)', 'Definition': '##############.#'},
            'CNES': {'type': CHAR(7), 'Description': 'Código CNES do estabelecimento de saúde (hospital)', 'Definition': '#######'},
        }
    },
    
    'Dimensão Paciente': {
        'tableNameInDataBase': 'dim_paciente',
        'columns': {
            'NASC': {'type': CHAR(8), 'Description': 'Data de nascimento do paciente', 'Definition': 'AAAAMMDD'},
            'SEXO': {'type': CHAR(1), 'Description': 'Sexo do paciente','Definition': '#', 'Values': '1: Masculino, 2: Feminino, 3: Feminino, 0-9: NA'},
            'IDADE': {'type': Numeric(2), 'Description': 'Idade do paciente na unidade do campo COD_IDADE', 'Definition': '##'},
            'COD_IDADE': {'type': CHAR(1), 'Description': 'Unidade de medida da idade', 'Definition': '#', 'Values': '0: ignorada, 2: dias, 3: meses, 4: anos, 5: mais de 100 anos'},
            'NACIONAL': {'type': CHAR(3), 'Description': 'Código do país de nascimento', 'Definition': '###'},
            'INSTRU': {'type': CHAR(1), 'Description': 'Grau de instrução do paciente', 'Definition': '#', 'Values': '1: Analfabeto, 2: 1° grau, 3: 2° grau, 4: 3° grau, 0-9: NA'},
            'RACA_COR': {'type': CHAR(2), 'Description': 'Raça/cor do paciente', 'Definition': '##', 'Values': '1: Branca, 2: Preta, 3: Parda, 4: Amarela, 5: Indígena, 0;99: NA'},
            'ETNIA': {'type': CHAR(4), 'Description': 'Etnia do paciente, se raça/cor for indígena', 'Definition': '####'},
            'CBOR': {'type': CHAR(3), 'Description': 'Ocupação do paciente, segundo a CBO (Classificação Brasileira de Ocupações)', 'Definition': '###'},
            'MORTE': {'type': Numeric(1), 'Description': 'Indicador de óbito do paciente', 'Definition': '#', 'Values': '1: Não, 2: Sim'},
        }
    },
    
    'Dimensão UTI': {
        'tableNameInDataBase': 'dim_uti',
        'columns': {
            'UTI_MES_TO': {'type': Numeric(3), 'Description': 'Total de dias de UTI durante a internação.', 'Definition': '###'},
            'MARCA_UTI': {'type': CHAR(2), 'Description': 'Indica qual o tipo de UTI utilizada pelo paciente', 'Definition': '##', 'Values': '01: Sim, 02: Não, 03: Ignorado'},
            'VAL_UTI': {'type': Numeric(8,2), 'Description': 'Valor referente aos gastos em UTI.', 'Definition': '########.##'},
        }
    },
    
    'Dimensão Procedimento': {
        'tableNameInDataBase': 'dim_procedimento',
        'columns': {
            'PROC_SOLIC': {'type': CHAR(10), 'Description': 'Procedimento solicitado', 'Definition': '##########'},
            'PROC_REA': {'type': CHAR(10), 'Description': 'Procedimento realizado', 'Definition': '##########'},
            'VAL_SH': {'type': Numeric(13,2) , 'Description': 'Valor do Serviço Hospitalar', 'Definition': '#############.##'},
            'VAL_SP': {'type': Numeric(13,2), 'Description': 'Valor do Serviço Profissional', 'Definition': '#############.##'},
            'N_AIH': {'type': CHAR(13), 'Description': 'Número da AIH (Autorização de Internação Hospitalar)', 'Definition': '#############'},
            'VAL_TOT': {'type': Numeric(14,2), 'Description': 'Valor total da AIH', 'Definition': '##############.##'},
            'INFEHOSP': {'type': CHAR(1), 'Description': 'Indicador de infecção hospitalar', 'Definition': '#', 'Values': '1: Sim, 2: Não, 3: Ignorado'},
            'IND_VDRL': {'type': CHAR(1), 'Description': 'Indica a execução do exame VDRL (Venereal Disease Research Laboratory - Estudo Laboratorial de Doenças Venéreas)', 'Definition': '#', 'Values': '0: Não executado, 1: Executado'},
        }
    },
    
    'Dimensão Diagnóstico': {
        'tableNameInDataBase': 'dim_diagnostico',
        'columns': {
            'DIAG_PRINC': {'type': CHAR(4), 'Description': 'Diagnóstico principal (CID10)', 'Definition': '####'},
            'DIAG_SECUN': {'type': CHAR(4), 'Description': 'Diagnóstico secundário (CID10)', 'Definition': '####'},
            'DIAGSEC1': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 1 (CID10)', 'Definition': '####'},
            'DIAGSEC2': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 2 (CID10)', 'Definition': '####'},
            'DIAGSEC3': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 3 (CID10)', 'Definition': '####'},
            'DIAGSEC4': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 4 (CID10)', 'Definition': '####'},
            'DIAGSEC5': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 5 (CID10)', 'Definition': '####'},
            'DIAGSEC6': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 6 (CID10)', 'Definition': '####'},
            'DIAGSEC7': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 7 (CID10)', 'Definition': '####'},
            'DIAGSEC8': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 8 (CID10)', 'Definition': '####'},
            'DIAGSEC9': {'type': CHAR(4), 'Description': 'Diagnóstico secundário 9 (CID10)', 'Definition': '####'},
            'CID_MORTE': {'type': CHAR(4), 'Description': 'CID10 do diagnóstico de morte', 'Definition': '####'},
            # 'CID_ASSO': {'type': CHAR(4), 'Description': 'CID10 do diagnóstico associado', 'Definition': '####'},
        }
        
    }
}

# Função para separar as dimensões do DataFrame
def separaDimensoes(dataFrame, dimensoes):

    # Inicializa o dicionário de dimensões
    dfs = {}
    
    for dim, dados in dimensoes.items():
        columns = dados['columns'].keys()
        
        # Cria um DataFrame com as colunas da dimensão
        df_dim = dataFrame[list(columns)]
        dfs[dados['tableNameInDataBase']] = df_dim
    
    return dfs
    

# df = pd.read_csv('Dados/csv/concatenacoes/concat_fev.csv', sep=';')

# dfs = separaDimensoes(df, dimensoes)