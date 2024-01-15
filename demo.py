from ASLD_step2.config import Configuration
from ASLD_step2.components import PrepareCallback,Training
from ASLD_step2 import logging

from ASLD_step2.Exception import ASLDException
import sys

STAGE_NAME = "Training"

def main():
    config = Configuration()
    prepare_callbacks_config = config.get_prepare_callback_config()
    prepare_callbacks = PrepareCallback(config=prepare_callbacks_config)
    callback_list = prepare_callbacks.get_tb_ckpt_callbacks()
    
    training_config = config.get_training_config()
    training = Training(config=training_config)
    training.get_base_model()
    training.train(
        callback_list=callback_list
    )
if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        raise ASLDException(e,sys) from e
