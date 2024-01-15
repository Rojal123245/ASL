import sys
sys.executable
import cv2
import mediapipe as mp
import os
import csv
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
mp_holistic = mp.solutions.holistic.Holistic()
videos_path = "C:\\Users\\saran\\OneDrive\\Desktop\\video_dummy_data\\"
output_path = "C:\\Users\\saran\\OneDrive\\Desktop\\extracted_landmarks_output\\"
class VideoProcessor:
        def __init__(self, videos_path, output_path):
                self.videos_path = videos_path
                self.output_path = output_path
                self.mp_holistic = mp.solutions.holistic.Holistic(static_image_mode=False)
        def process_videos(self):
                # Create a list to store the video analysis results
                video_results = []
                # Iterate over the videos in the videos_path
                for filename in os.listdir(self.videos_path):
                        if filename.endswith(".mp4"):
                                video_path = os.path.join(self.videos_path, filename)
                                video_name = os.path.splitext(filename)[0]
                                
                                # Open the video

                                cap = cv2.VideoCapture(video_path)

                                # Process each frame in the video

                                while cap.isOpened():
                                        ret, frame = cap.read()
                                        if not ret:
                                                break

                                        # Perform holistic analysis using Mediapipe
                                        with self.mp_holistic as holistic:
                                                results = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                                        if results is not None:
                                                video_results.append((video_name, results))
                                        else:
                                                video_results.append((video_name, None))
                                        # Store the analysis results in a list

                                        video_results.append((video_name, results))
                                        
                                        # Visualize the results on the frame
                                        if results.pose_landmarks:
                                                mp.solutions.drawing_utils.draw_landmarks(
                                                        frame,
                                                        results.pose_landmarks,
                                                        mp.solutions.holistic.POSE_CONNECTIONS
                                                )
                                        if results.left_hand_landmarks:
                                                mp.solutions.drawing_utils.draw_landmarks(
                                                        frame,
                                                        results.left_hand_landmarks,
                                                        mp.solutions.holistic.HAND_CONNECTIONS
                                                )
                                        if results.right_hand_landmarks:
                                                mp.solutions.drawing_utils.draw_landmarks(
                                                        frame,
                                                        results.right_hand_landmarks,
                                                        mp.solutions.holistic.HAND_CONNECTIONS
                                                )
                                        # Display the frame with landmarks
                                        cv2.imshow('Frame', frame)
                                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                                break
                                # Release the video capture object
                                cap.release()
                                cv2.destroyAllWindows()
                                
                        # Save the video analysis results to a Parquet file
                        video_data = pa.Table.from_pandas(pd.DataFrame(video_results, columns=["Video", "Results"]))
                        pq.write_table(video_data, os.path.join(self.output_path, "video_results.parquet"))
                        print("Executed")

import cv2
import mediapipe as mp
import numpy as np
class LandmarkDetector:
    def __init__(self, model):
        self.mp_holistic = model
    
    def detect_landmarks(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        results = self.mp_holistic.process(frame_rgb)
        frame_rgb.flags.writeable = True
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        return frame_bgr, results
    
    def landmark_extraction(self, results):
        pose = np.array([[coordinate.x, coordinate.y, coordinate.z, coordinate.visibility] for coordinate in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
        left_hand = np.array([[coordinate.x, coordinate.y, coordinate.z] for coordinate in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
        right_hand = np.array([[coordinate.x, coordinate.y, coordinate.z] for coordinate in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
        face = np.array([[coordinate.x, coordinate.y, coordinate.z] for coordinate in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
        return np.concatenate([pose, left_hand, right_hand, face])

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.mp_holistic = mp.solutions.holistic.Holistic()
        self.detector = LandmarkDetector(self.mp_holistic)
        
        if not self.cap.isOpened():
            print("Failed to open the video file.")

    def process_video(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            processed_frame, results = self.detector.detect_landmarks(frame)
            landmarks = self.detector.landmark_extraction(results)
            cv2.imshow('Processed Frame', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

video_path = r'C:\Users\saran\OneDrive\Desktop\video_dummy_data\00384.mp4'
video_processor = VideoProcessor(video_path)
video_processor.process_video()

class ParquetWriter:
    def __init__(self, landmarks_path, id_dict):
        self.landmarks_path = landmarks_path
        self.id_dict = id_dict

    def write(self, np_array, video_id):
        np_array_flat = np_array.flatten()
        pa_array = pa.array(np_array_flat)
        table = pa.Table.from_arrays([pa_array], names=[self.id_dict[video_id]])
        writer = pq.ParquetWriter(self.landmarks_path + video_id + '.parquet', table.schema)
        writer.write_table(table)
        writer.close()
        return

class VideoProcessor:
    def __init__(self, videos_path, landmarks_path):
        self.videos_path = videos_path
        self.landmarks_path = landmarks_path
        self.mp_holistic = mp.solutions.holistic

    def process_videos(self):
        for item in os.listdir(self.videos_path):
            if item.endswith('.mp4'):  
                cap = cv2.VideoCapture(os.path.join(self.videos_path, item))

                # List that will receive the landmark's coordinates for each video
                landmarks_list = []

                # Set mediapipe model
                with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                    # Looping through all the frames
                    while cap.isOpened():  
                        # Reading the frames
                        ret, frame = cap.read()
                        if not ret: 
                            break
                        # Making detections
                        image, results = self.landmark_detection(frame, holistic)
                        landmarks_list.append(self.landmark_extraction(results))

                        cv2.waitKey(10)
                    cap.release()
                    cv2.destroyAllWindows()

                # Saving the NumPy array
                np.save(os.path.join(self.landmarks_path, item.split(".mp4")[0]), np.array(landmarks_list))

                # Converting and storing the array into parquet file
                self.parquet_writer(np.array(landmarks_list), item.split('.mp4')[0])

    def landmark_detection(self, frame, model):
        # Color conversion 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        frame.flags.writeable = False  
        results = model.process(frame)  
        frame.flags.writeable = True  
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
        return frame, results

    def landmark_extraction(self, results):
        pose = np.array([[coordinate.x, coordinate.y, coordinate.z, coordinate.visibility] for coordinate in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
        left_hand = np.array([[coordinate.x, coordinate.y, coordinate.z] for coordinate in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
        right_hand = np.array([[coordinate.x, coordinate.y, coordinate.z] for coordinate in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
        face = np.array([[coordinate.x, coordinate.y, coordinate.z] for coordinate in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
        return np.concatenate([pose, left_hand, right_hand, face])
    def parquet_writer(self, np_array, video_id):
        np_array_flat = np_array.flatten()
        pa_array = pa.array(np_array_flat)  
        table = pa.Table.from_arrays([pa_array], names=[video_id])  
        writer = pq.ParquetWriter(os.path.join(self.landmarks_path, video_id + '.parquet'),
                                  table.schema) 
        writer.write_table(table)  
        writer.close()  


videos_path = "C:\\Users\\saran\\OneDrive\\Desktop\\video_dummy_data\\"
landmarks_path = "C:\\Users\\saran\\OneDrive\\Desktop\\extracted_landmarks_output\\"

video_processor = VideoProcessor(videos_path, landmarks_path)
video_processor.process_videos()



                        
