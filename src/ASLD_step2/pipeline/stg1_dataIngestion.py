from ASLD_step2.config import Configuration
from ASLD_step2.components import DataIngestion
from ASLD_step2 import logging

from ASLD_step2.Exception import ASLDException
import sys

STAGE_NAME = "Data Ingestion stage"

def main():
    config = Configuration()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(config = data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.check_and_extract_files()
    data_ingestion.train_test_split()


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        raise ASLDException(e,sys) from e
