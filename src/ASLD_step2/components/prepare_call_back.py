import os
from ASLD_step2.entity import PrepareCallbacksConfig
import tensorflow as tf
import time
import os
import time

class PrepareCallback:
    def __init__(self, config: PrepareCallbacksConfig):
        self.config = config

    @property
    def _create_tensorboard_callback(self):
        tb_running_log_dir = os.path.join(self.config.tensorboard_root_log_dir,time.strftime("%Y%m%d-%H%M%S"))
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)
        return tensorboard_callback
    

    @property
    def _create_ckpt_callbacks(self):
        checkpoint_model_filepath = str(self.config.checkpoint_model_filepath)  # Convert to string if it's a PosixPath object
        
        return tf.keras.callbacks.ModelCheckpoint(
                filepath=checkpoint_model_filepath, 
                save_best_only=True
            )
         
    def get_tb_ckpt_callbacks(self):
        return [
            self._create_tensorboard_callback,
            self._create_ckpt_callbacks
        ]