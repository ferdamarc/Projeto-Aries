#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Scheduler para os Subsistemas ETL do Projeto ARIES

Este script realiza o agendamento da execucao dos subsistemas de ETL:
- subsystem_extract: Extracao de dados do SIH/SUS
- subsystem_trans: Transformacao e carga dos dados extraidos
"""

import time
import schedule
import sys
import logging
import os
from datetime import datetime

# Importar os subsistemas
# from subsystem_extract import extract_and_load
from subsystem_trans import main as transform_and_load

# Função para gerar o nome do arquivo de log com a data atual
def get_log_filename():
    # Obter a data atual no formato YYYY-MM-DD
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Criar o caminho completo para o arquivo de log com a data
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    # Certificar-se de que o diretório existe
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, f"etl_scheduler_{current_date}.log")

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(get_log_filename()),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("ETL_Scheduler")

def executar_pipeline_completo():
    """Executa a pipeline ETL completa, com extracao, transformacao e carga"""
    logger.info("Iniciando pipeline ETL")
    
    # Comentado pois no wind não dá p utilizar o pysus
    # Extração
    # logger.info("Iniciando extracao de dados")
    # try:
    #     extracao_sucesso = extract_and_load()
    #     if not extracao_sucesso:
    #         logger.warning("Extracao completou com avisos. Continuando com a transformacao...")
    # except Exception as e:
    #     logger.error(f"Erro durante a extracao: {e}")
    #     logger.warning("Tentando continuar com a transformacao mesmo assim...")
    
    # Transformação e Carga
    logger.info("Iniciando transformacao e carga de dados")
    try:
        transform_and_load()
        logger.info("Pipeline ETL concluido com sucesso!")
    except Exception as e:
        logger.error(f"Erro durante a transformacao e carga: {e}")

def configurar_agendamento():
    """Configura o agendamento da execucao do pipeline ETL"""
    hour = "21:59"
    schedule.every().day.at(hour).do(executar_pipeline_completo)
    
    logger.info(f"Agendamento configurado. O pipeline sera executado diariamente as {hour}h.")
    logger.info("O scheduler esta em execucao. Pressione Ctrl+C para interromper.")

def main():
    """Função principal"""
    logger.info("Iniciando o scheduler ETL")
    
    configurar_agendamento()
    
    # Executar imediatamente na primeira vez (apenas para debugar)
    executar_pipeline_completo()
    
    # Loop principal do scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto; está funcionando pois já testei
    except KeyboardInterrupt:
        logger.info("Scheduler interrompido pelo usuario.")
    except Exception as e:
        logger.error(f"Erro no scheduler: {e}")

if __name__ == "__main__":
    main()
