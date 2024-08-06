#"""This program works as mouse curser by tracking your hand """#
#"""To perform LEFT CLICK link Index finger & Thumb finger """#
#"""To perform RIGHT CLICK link Ring finger & Thumb finger"""#
#"""To STOP Program press 'x' key"""#
import cv2  # cv2 is for video capturing
import mediapipe as m  # mediapipe is for landmarks
import win32api  # Copy move and delete files using the built in Window's progress dialog
import pyautogui  # To mouse control and other GUI automation tasks.
import math

m_drawing = m.solutions.drawing_utils
m_hands = m.solutions.hands
click = 0

video = cv2.VideoCapture(0)

with m_hands.Hands(min_detection_confidence = 0.8 , min_tracking_confidence = 0.8) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # To set the frame size to video

        image = cv2.flip(image, 1)  # To flip the video and 1 is to flip the vidro one time

        imageHeight, imageWidth, _ = image.shapex

        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            # enumerate : count of iterations
            for num, hand in enumerate(results.multi_hand_landmarks):
                # To control the thinkness and circle radius of points
                m_drawing.draw_landmarks(image, hand, m_hands.HAND_CONNECTIONS,
                                         m_drawing.DrawingSpec(color=[0, 0, 0], thickness=8, circle_radius=10),)

        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                for point in m_hands.HandLandmark:

                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = m_drawing._normalized_to_pixel_coordinates(
                        normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)

                    point = str(point)

                    if point == 'HandLandmark.INDEX_FINGER_TIP':
                        try:
                            indexfingertip_x = pixelCoordinatesLandmark[0]
                            indexfingertip_y = pixelCoordinatesLandmark[1]
                            win32api.SetCursorPos((indexfingertip_x * 4, indexfingertip_y * 5))


                        except:
                            pass

                    elif point == 'HandLandmark.RING_FINGER_TIP':
                        try:
                            ringfingertip_x = pixelCoordinatesLandmark[0]
                            ringfingertip_y = pixelCoordinatesLandmark[1]
                            win32api.SetCursorPos((ringfingertip_x * 4, ringfingertip_y * 5))


                        except:
                            pass

                    elif point == 'HandLandmark.THUMB_TIP':
                        try:
                            thumbfingertip_x = pixelCoordinatesLandmark[0]
                            thumbfingertip_y = pixelCoordinatesLandmark[1]

                        except:
                            pass

                    try:

                        Dis_x = math.sqrt((indexfingertip_x-thumbfingertip_x)**2 + (indexfingertip_x-thumbfingertip_x)**2)
                        Dis_y = math.sqrt((indexfingertip_y-thumbfingertip_y)**2 + (indexfingertip_y-thumbfingertip_y)**2)

                        if Dis_x < 5 or Dis_x < -5:
                            if Dis_y < 5 or Dis_y < -5:
                                click += 1
                                if click % 5 == 0:
                                    print("Left Click Perfromed")
                                    pyautogui.click()
                                    continue

                    except:
                        pass

                    try:

                        Dis_x = math.sqrt((ringfingertip_x - thumbfingertip_x) ** 2 + (ringfingertip_x - thumbfingertip_x) ** 2)
                        Dis_y = math.sqrt((ringfingertip_y - thumbfingertip_y) ** 2 + (ringfingertip_y - thumbfingertip_y) ** 2)

                        if Dis_x < 5 or Dis_x < -5:
                            if Dis_y < 5 or Dis_y < -5:
                                click += 1
                                if click % 5 == 0:
                                    print("Right Click Performed")
                                    pyautogui.rightClick()
                                    continue
                    except:
                        pass


        cv2.imshow('HTC [HAND TRACKING CURSOR]', image)  # imshow("Title", tab)

        if cv2.waitKey(100) & 0xFF == ord('x'):
            break

video.release()