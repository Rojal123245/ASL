"""
author:
time:
this class is created to retrive the data ,extract the data ,and split the data into train and test 
since we have assigned properties to entity we can use those entity here to perform all those task
"""

from ASLD_step2.entity import DataIngestionConfig
from ASLD_step2.logger import logging
from ASLD_step2.Exception import ASLDException
import sys
import os
import urllib.request as request
from pathlib import Path
from ASLD_step2.utils import get_size
from zipfile import ZipFile
import pandas as pd
import os
import shutil
from sklearn.model_selection import train_test_split
import json
from ASLD_step2.constants import *
import numpy as np
from tqdm import tqdm

from sklearn.preprocessing import LabelBinarizer

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.label_binarizer = LabelBinarizer()

    def download_file(self):
    #this function will download the file and store in local_data_file
        try:
            logging.info('Trying to download file')
            #urlretrieve needs url and path to store file
            logging.info("Trying to download file...")

            if not os.path.exists(self.config.local_data_file):

                logging.info("Download started...")
                filename, headers = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=self.config.local_data_file
                )
                logging.info(f"{filename} download! with following info: \n{headers}")
            else:
                 logging.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")  

        except Exception as e:
            raise ASLDException(e,sys) from e



    def check_and_extract_files(self):
        """
        Check if the artifact/videos folder is empty. If empty, unzip video data from WLASL_videos.zip
        and move only video files into artifact/videos. Then delete the unzip folder. If not empty, return.
        """
        try:
    
            if os.path.exists(self.config.unzip_dir):
                # Unzip video data from WLASL_videos.zip
                with ZipFile(self.config.local_data_file, 'r') as zip_ref:
                    zip_ref.extractall(self.config.unzip_dir)
                logging.info("extraction completed")
            else:
                logging.info("error in Extraction...")
        except Exception as e:
            raise ASLDException(e,sys) from e
        


    """
    creating a function to associate the words to a unique number with json file.
    """    

    def map_json_unique_number(self,json_file):
        #getting the path of json file
        try:
            json_file_path = os.path.join(self.config.unzip_dir,json_file)
            with open(json_file_path, 'r') as j:
                logging.info("associate the words to a unique number with json file")
            
                return json.loads(j.read())
            
        except Exception as e:
            raise ASLDException(e,sys) from e    
        
    """
    Loading all the landmarks

    """
    
    def load_landmarks(self):
        # Getting the files to load
        try:
            train_csv_path = os.path.join(self.config.unzip_dir, TRAIN_CSV)
            #read the csv
            train_csv = pd.read_csv(train_csv_path)
            # get the path of csv file
            train_file_path = self.config.unzip_dir+"/"+train_csv['path'].values#[:2000]
            word = train_csv['sign'].values#[:2000]

            # Columns to upload
            data_columns = ['x', 'y']

            landmarks = np.empty((train_file_path.shape[0], NUM_FRAMES, DESIRED_NUM_ROWS), dtype=float)
            labels = []
            
            for i in tqdm(range(train_file_path.shape[0])):

                # Loading the train_file_path
                data = pd.read_parquet(train_file_path[i], columns=data_columns).fillna(0)
                num_frames = int(len(data) / TOTAL_ROWS)
                data = data.values.reshape(num_frames, TOTAL_ROWS, len(data_columns))
                data.astype(np.float32)

                # Dropping undesired points
                data = data[:, LANDMARKS_TO_KEEP]

                # Adjusting the number of frames
                if data.shape[0] > NUM_FRAMES:  # time-based sampling
                    indices = np.arange(0, data.shape[0], data.shape[0] // NUM_FRAMES)[:NUM_FRAMES]
                    data = data[indices]
                elif data.shape[0] < NUM_FRAMES:  # padding the videos
                    rows = NUM_FRAMES - data.shape[0]
                    data = np.append(np.zeros((rows, len(LANDMARKS_TO_KEEP), len(data_columns))), data, axis=0)

                # Reshaping the data
                landmarks[i] = data.reshape(NUM_FRAMES, len(LANDMARKS_TO_KEEP) * len(data_columns), order='F')
                del data
                sign_dict = self.map_json_unique_number(JSON_FILE)

                # Creating the labels dataset
                labels.append(sign_dict[word[i]])
            return landmarks, np.array(labels)
        except Exception as e:
            raise ASLDException(e,sys) from e


    def train_test_split(self):
        try:
            x_train, y_train = self.load_landmarks()

            x_train, x_val_test, y_train, y_val_test = train_test_split(x_train, y_train, test_size=0.1, random_state=42)
            x_val, x_test, y_val, y_test = train_test_split(x_val_test, y_val_test, test_size=0.5, random_state=42)
            y_train = self.label_binarizer.fit_transform(y_train)
            y_val = self.label_binarizer.transform(y_val)
            np.save(os.path.join(self.config.train_dir, "x_train.npy"), x_train)
            np.save(os.path.join(self.config.train_dir, "y_train.npy"), y_train)
            np.save(os.path.join(self.config.test_dir, "x_val.npy"), x_val)
            np.save(os.path.join(self.config.test_dir, "y_val.npy"), y_val)
            logging.info("train and validation data saved into directory")
        except Exception as e:
                raise ASLDException(e,sys) from e

    

