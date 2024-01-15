"""
author: @kumar Dahal
time: Jun 11 2023
this class is created to assamble entity and properties(config/config.yaml) 
and will return path to entity
"""
from ASLD_step2.constants import *
from ASLD_step2.utils import read_yaml,create_directories
from ASLD_step2.entity import DataIngestionConfig,PrepareBaseModelConfig,PrepareCallbacksConfig,TrainingConfig,EvaluationConfig
from ASLD_step2.Exception import ASLDException
from ASLD_step2.constants import *
import sys


class Configuration:
    def __init__(self,
                config_filepath = CONFIG_FILE_PATH,
                params_filepath = PARAMS_FILE_PATH
                ):
        #reading the config.yaml file by importing from constants
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
    
        #creating parent directories entity
        create_directories([self.config.artifacts_root])


    """
    this function is written to create the skeletion of DataIngestion entity 
    and will return path for DataIngestionConfig
    """  
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        #read config file to get data_ingestion attributes of DataIngestion
        try:
            config = self.config.data_ingestion
            #create directories for attributes of data_ingestion
            create_directories([config.root_dir])
            create_directories([config.train_dir])
            create_directories([config.test_dir])
            
            #assign the entity with its properities and return it
            data_ingestion_config = DataIngestionConfig(
                root_dir = config.root_dir,
                source_URL = config.source_URL,
                local_data_file = config.local_data_file,
                unzip_dir = config.unzip_dir,
                train_dir = config.train_dir,
                test_dir = config.test_dir
            )

            return data_ingestion_config  
        except Exception as e:
            raise ASLDException(e,sys) from e
        


    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
            config = self.config.prepare_base_model
            
            create_directories([config.root_dir])

            prepare_base_model_config = PrepareBaseModelConfig(
                root_dir=Path(config.root_dir),
                base_model_path=Path(config.base_model_path),
                params_final_output_layers= self.params.FINAL_OUTPUT_CLASS
            )

            return prepare_base_model_config

    def get_prepare_callback_config(self) -> PrepareCallbacksConfig:
        config = self.config.prepare_callbacks
        model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
        create_directories([
            Path(model_ckpt_dir),
            Path(config.tensorboard_root_log_dir)
        ])

        prepare_callback_config = PrepareCallbacksConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath)
        )

        return prepare_callback_config
    
    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params

        x_train_path = os.path.join(self.config.data_ingestion.train_dir,X_TRAIN)

        y_train_path = os.path.join(self.config.data_ingestion.train_dir,Y_TRAIN)

        x_val_path = os.path.join(self.config.data_ingestion.test_dir,X_VAL)

        y_val_path = os.path.join(self.config.data_ingestion.test_dir,Y_VAL)


        create_directories([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            base_model_path=Path(prepare_base_model.base_model_path),
            params_epochs=params.EPOCHS,
            x_train= x_train_path,
            y_train= y_train_path,
            x_val= x_val_path,
            y_val= y_val_path,
        )

        return training_config    
    

    def get_validation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model=self.config.training.trained_model_path,
            training_data=os.path.join(self.config.data_ingestion.unzip_dir,'ASL_Dataset','Train'),

        )
        return eval_config




