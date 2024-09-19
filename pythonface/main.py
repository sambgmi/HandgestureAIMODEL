import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image
import streamlit as st 
 
st.set_page_config(layout="wide")
st.image('MathGestures.png')
 
col1, col2 = st.columns([3,2])
with col1:
    run = st.checkbox('Run', value=True)
    FRAME_WINDOW = st.image([])
 
with col2:
    st.title("Answer")
    output_text_area = st.subheader("")
 
genai.configure(api_key="AIzaSyByjH_2-T0HAM5tI5JFN0ar4J3-flrwViw")
model = genai.GenerativeModel('gemini-1.5-flash')
 
# Initialize the webcam to capture video
# The '2' indicates the third camera connected to your computer; '0' would usually refer to the built-in camera
cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
 
# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)
 
 


def sendToAI(model,canvas,fingers):
    if fingers == [1,1,1,1,0]:
        pil_image = Image.fromarray(canvas)
        response = model.generate_content(["Solve this math problem", pil_image])
        return response.text
 
 
prev_pos= None
canvas=None
image_combined = None
output_text= ""
# Continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
 
    if canvas is None:
        canvas = np.zeros_like(img)
 
 
    info = getHandInfo(img)
    if info:
        fingers, lmList = info
        prev_pos,canvas = draw(info, prev_pos,canvas)
        output_text = sendToAI(model,canvas,fingers)
 
    image_combined= cv2.addWeighted(img,0.7,canvas,0.3,0)
    FRAME_WINDOW.image(image_combined,channels="BGR")
 
    if output_text:
        output_text_area.text(output_text)
 
    # # Display the image in a window
    # cv2.imshow("Image", img)
    # cv2.imshow("Canvas", canvas)
    # cv2.imshow("image_combined", image_combined)
 
 
    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    cv2.waitKey(1)