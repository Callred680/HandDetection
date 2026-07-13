import cv2
import mediapipe as MP
import numpy as np
import traceback

import HandDetectionMethods as HDM

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                   WINDOW VARIABLES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
WINDOW_NAME = "Controllable Window"

WINDOW_X = 300
WINDOW_Y = 200
SCREEN_WIDTH = 3840 # Equates to the width of double monitor system (1920x1080)
SCREEN_HEIGHT = 1080
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300

MIN_WIDTH = 300
MAX_WIDTH = 1000
MIN_HEIGHT = 200
MAX_HEIGHT = 700

RESIZE_SPEED = 6
MOVE_SPEED = 9

LAST_DIRECTION = ""
DIRECTION_COUNT = 0

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    MAIN PROGRAM 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def Check_Direction(direction):
    global LAST_DIRECTION, DIRECTION_COUNT, WINDOW_X, WINDOW_Y

    # Move window based on directed gesture
    if direction == LAST_DIRECTION:
        DIRECTION_COUNT += 1
    else:
        DIRECTION_COUNT = 1
        LAST_DIRECTION = direction

    if DIRECTION_COUNT >= 5:
        if direction == "LEFT":
            WINDOW_X -= MOVE_SPEED
        elif direction == "RIGHT":
            WINDOW_X += MOVE_SPEED
        elif direction == "DOWN":
            WINDOW_Y += MOVE_SPEED
        elif direction == "UP":
            WINDOW_Y -= MOVE_SPEED

        # This prevents window from leaving frame
        WINDOW_X = max(0, min(WINDOW_X, SCREEN_WIDTH))
        WINDOW_Y = max(0, min(WINDOW_Y, SCREEN_HEIGHT))

def Check_Gesture(gesture):
    global WINDOW_HEIGHT, WINDOW_WIDTH, RESIZE_SPEED

    if gesture == "OPEN":
        WINDOW_HEIGHT += RESIZE_SPEED
        WINDOW_WIDTH += RESIZE_SPEED
    elif gesture == "CLOSED":
        WINDOW_HEIGHT -= RESIZE_SPEED
        WINDOW_WIDTH -= RESIZE_SPEED
    else:
        return
    
    # Check if boundaries for window size are met
    WINDOW_WIDTH = max(MIN_WIDTH, min(WINDOW_WIDTH, MAX_WIDTH))
    WINDOW_HEIGHT = max(MIN_HEIGHT, min(WINDOW_HEIGHT, MAX_HEIGHT))


# Initialize webcam (0 = default camera)
CAMERA = cv2.VideoCapture(0)
    
# Initialize hand detection model
mpHands = MP.solutions.hands
HANDS = mpHands.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.75, min_tracking_confidence = 0.75)
mpDraw = MP.solutions.drawing_utils
# Establish default location for camera frame
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.moveWindow(WINDOW_NAME, WINDOW_X, WINDOW_Y)

try:
    # Capture camera footage
    while True:
        # Read frame by frame (success == true if frame is read correctly)(frame == image)
        success, frame = CAMERA.read()

        # Verify frame was successfully captured through success
        if not success:
            print("Error receiving frame")
            break

        # Flip camera for more natural feel
        frame = cv2.flip(frame, 1)
        
        hands_detected = HANDS.process(frame)   # Detect hand

        # Once detected, locate keypoints and highlight the dots
        if hands_detected.multi_hand_landmarks:

            # Iterate through each 
            for HandLandMarks in hands_detected.multi_hand_landmarks:
                height, width, channel = frame.shape    # return a tuple of frame size and number of color components

                '''    CODE FOR DRAWING CONNECTED DOTS ACROSS ALL LANDMARKS IN DETECTED HAND
                # Assign id to respective landmark
                for id, landmark in enumerate(HandLandMarks.landmark):
                    channel_x, channel_y = int(landmark.x * width), int(landmark.y * height)
                    cv2.circle(frame, (channel_x, channel_y), 3, (255,0,255), cv2.FILLED)   # This is creating a filled circle on the respective landmark point
                mpDraw.draw_landmarks(frame, HandLandMarks, mpHands.HAND_CONNECTIONS)   # This connects the dots
                '''

                base = HandLandMarks.landmark[5]
                tip = HandLandMarks.landmark[8]
                x1 = int(base.x * width)
                y1 = int(base.y * height)

                x2 = int(tip.x * width)
                y2 = int(tip.y * height)

                cv2.circle(frame, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 8, (0, 0, 255), cv2.FILLED)

                cv2.arrowedLine(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

                # Get status of open/closed hand
                gesture = HDM.Get_Gesture(HandLandMarks)
                # Get indicated direction for directional control of window
                direction = HDM.Get_Direction(HandLandMarks)

                # Display direction with arrow along with drawn arrow on finger
                cv2.putText(frame, "Direction: " + direction, (10,75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                # Display if palm is open or closed
                cv2.putText(frame, "Palm State: " + gesture, (10,115), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

                # Check if palm is opened or closed first to prevent over lap of frame changes
                if gesture == "OTHER" :
                    Check_Direction(direction)
                else:
                    Check_Gesture(gesture)

                # Move and adjust sizing/position of camera and frame
                cv2.moveWindow(WINDOW_NAME, WINDOW_X, WINDOW_Y)
                frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
                cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

        frame = HDM.FPS_Counter(frame)

        cv2.imshow(WINDOW_NAME, frame) # Display image
        if cv2.waitKey(1) == ord('q'):
            CAMERA.release() # Releases camera
            cv2.destroyAllWindows() # Destroys all opened windows
            break

except Exception:
    traceback.print_exc()
    CAMERA.release() # Releases camera
    cv2.destroyAllWindows() # Destroys all opened windows






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                    ================== READ ME INFORMATION ==================

1. This code utilizes mediapipe version 0.10.21 specifically due to the use of 'MP.solutions.hands'
    - To download respective library (python -m pip install mediapipe==0.10.21)
2. The mediapipe library is used in recognizing the specific landmarks on the hands (set to recognize max 1 for performance)
    - Uses single-shot palm detection model for key point localization of 21 3D palm coordinates (lower number = closer to wrist for respective finger)
        0. Wrist
            1. Thumb_cmc        5. Index_finger_mcp     9. Middle_finger_mcp        13. Ring_finger_mcp       17. Pinky_mcp
            2. Thumb_mcp        6. Index_finger_pip     10. Middle_finger_pip       14. Ring_finger_pip       18. Pinky_pip
            3. Thumb_ip         7. Index_finger_dip     11. Middle_finger_dip       15. Ring_finger_dip       19. Pinky_dip
            4. Thumb_tip        8. Index_finger_tip     12. Middle_finger_tip       16. Ring_finger_tip       20. Pinky_tip
    - Landmarks are mapped to an array of detected digits
        - [Thumb, Index, Middle, Ring, Pinky]
3. This code will be a compilation of related computer vision and ai/ml models
    - Key features
        = FPS counter
        = Hand detection
        = Hand recognition (i.e. printing left, right, closed, open, etc.)
        = Controllable simple game
            > Pong?
4. TODO
    - Separate functions into specifc modules/classes
    - Create detection feature for hand signals
    - Create simple game
    - Translate motion controls into game


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""