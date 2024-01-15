#Importing necessery libraries
import os
import tensorflow as tf
import cv2
import mediapipe as mp
from keras.models import load_model
import numpy as np
import time
#Loading the pre trainned model
model = load_model('smnist.h5')
#defining variables for Mediapipe hands and webcam campture
mphands = mp.solutions.hands
hands = mphands.Hands()
cap = cv2.VideoCapture(0)
def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, (28, 28))
    normalized_image = resized_image / 255.0
    batched_image = np.expand_dims(normalized_image, axis=0)
    final_image = np.expand_dims(batched_image, axis=-1)
    return final_image
while True:
    # Reading image from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame from camera.")
        break

    # Flip the image horizontally
    frame = cv2.flip(frame, 1)

    # Processing the image with Mediapipe hands to detect hand landmarks
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    hand_landmarks = result.multi_hand_landmarks
    if hand_landmarks:
        for handLMs in hand_landmarks:
            x_max, y_max = 0, 0
            x_min, y_min = frame.shape[1], frame.shape[0]

            for lm in handLMs.landmark:
                x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
            # Adding pixels to the bounding box to include more context
            y_min -= 20
            y_max += 20
            x_min -= 20
            x_max += 20


            # Drawing the bounding box on the frame
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Croping the region of interest for prediction
            analysis_frame = frame[y_min:y_max, x_min:x_max]
            pixel_data = preprocess_image(analysis_frame)

            # Making the prediction using the loaded model
            prediction = model.predict(pixel_data)
            pred_array = np.array(prediction[0])
            letter_pred = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

            # Finding the top 3 predicted characters and their confidences
            pred_array_ordered = np.argsort(pred_array)[::-1]
            for i in range(3):
                idx = pred_array_ordered[i]
                predicted_char = letter_pred[idx]
                confidence = pred_array[idx]
                print(f"Predicted Character {i+1}: {predicted_char}")
                print(f"Confidence {i+1}: {confidence*100:.2f}%")

    # Showing the frame with the predicted results
    cv2.imshow("Frame", frame)

    # ESC key press to exit
    k = cv2.waitKey(1)
    if k % 256 == 27:
        print("Escape hit, closing...")
        break

# Releasing the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()