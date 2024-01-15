from ASLD_step2.entity import TrainingConfig
import tensorflow as tf
from pathlib import Path
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def get_base_model(self):
        self.model = tf.keras.models.load_model(
            self.config.base_model_path
        )
  

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)


    def train(self, callback_list: list):
        y_val_load = np.load(self.config.y_val)
        x_val_load = np.load(self.config.x_val)
        x_train_load = np.load(self.config.x_train)
        y_train_load = np.load(self.config.y_train)
        
        self.model.fit(x_train_load, 
                       y_train_load, 
                       epochs=self.config.params_epochs, 
                       validation_data=(x_val_load, y_val_load), 
                       callbacks=callback_list
                       )

        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )