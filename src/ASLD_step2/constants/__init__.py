"""
author:@ kumar dahal
date: june 6 2023
"""
import os
from datetime import datetime
from pathlib import Path

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"



CONFIG_FILE_PATH = Path("configs/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")

NUM_FRAMES = 30

JSON_FILE  ='sign_to_prediction_index_map.json'
TRAIN_CSV = 'train.csv'

FACE_KEEP_POINTS = [0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146, 61, 185, 40, 39, 37]
FACE_KEEP_POINTS.sort()
LEFT_HAND_KEEP_POINTS = [i for i in range(21)]
POSE_KEEP_POINTS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24]
RIGHT_HAND_KEEP_POINTS = [i for i in range(21)]

FACE_KEEP_IDX = [FACE_KEEP_POINTS[i] for i in range(len(FACE_KEEP_POINTS))]
LEFT_HAND_KEEP_IDX = [i + 468 for i in LEFT_HAND_KEEP_POINTS]
POSE_KEEP_INDX = [i + 468 + 21 for i in POSE_KEEP_POINTS]
RIGHT_HAND_KEEP_IDX = [i + 468 + 21 + 33 for i in RIGHT_HAND_KEEP_POINTS]

LANDMARKS_TO_KEEP = FACE_KEEP_IDX + LEFT_HAND_KEEP_IDX + POSE_KEEP_INDX + RIGHT_HAND_KEEP_IDX

del FACE_KEEP_POINTS, LEFT_HAND_KEEP_POINTS, POSE_KEEP_POINTS, RIGHT_HAND_KEEP_POINTS
del FACE_KEEP_IDX, LEFT_HAND_KEEP_IDX, POSE_KEEP_INDX, RIGHT_HAND_KEEP_IDX

TOTAL_ROWS = 543
DESIRED_NUM_ROWS = len(LANDMARKS_TO_KEEP) * 2

X_TRAIN = 'x_train.npy'
Y_TRAIN = 'y_train.npy'
X_VAL =  'x_val.npy'
Y_VAL = 'x_val.npy'





