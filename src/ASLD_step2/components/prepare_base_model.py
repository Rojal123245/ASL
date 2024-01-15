from ASLD_step2.config import configurations
import os
from ASLD_step2.Exception import ASLDException
import sys
from ASLD_step2.logger import logging
import tensorflow as tf
from ASLD_step2.entity import PrepareBaseModelConfig
from pathlib import Path

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    @staticmethod
    def build_base_model(final_output_class):
        inputs = tf.keras.layers.Input(shape =(None, 158))

        x = tf.keras.layers.Dense(256)(inputs)
        x = tf.keras.layers.LayerNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)
        x = tf.keras.layers.Dropout(0.5)(x)

        x = tf.keras.layers.Dense(128)(x)
        x = tf.keras.layers.LayerNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)
        x = tf.keras.layers.Dropout(0.5)(x)

        x = tf.keras.layers.Dense(256)(x)
        x = tf.keras.layers.LayerNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)
        x = tf.keras.layers.Dropout(0.5)(x)

        lstm_output = tf.keras.layers.LSTM(256)(x)

        outputs = tf.keras.layers.Dense(final_output_class, activation='softmax')(lstm_output)

        model = tf.keras.Model(inputs=inputs,
                                outputs=outputs
                            )

        model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
            )

        model.summary()
        return model
    
    #call the function to save model and function to create an architecture of an model
    def create_base_model(self):
        self.model = self.build_base_model(
            final_output_class=self.config.params_final_output_layers

        )

        self.save_model(path=self.config.base_model_path, model=self.model)

    #functio to save the model
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
            model.save(path)
