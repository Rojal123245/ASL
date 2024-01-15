from ASLD_step2.config import Configuration
from ASLD_step2.components import DataIngestion,PrepareBaseModel
from ASLD_step2 import logging

from ASLD_step2.Exception import ASLDException
import sys


STAGE_NAME = "Prepare base model"

def main():
    config = Configuration()
    prepare_base_model_config = config.get_prepare_base_model_config()
    prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
    prepare_base_model.create_base_model()

if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        raise ASLDException(e,sys) from e