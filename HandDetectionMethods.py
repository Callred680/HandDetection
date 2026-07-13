import cv2
import time

# Variables for tracking time passed to calculate FPS
PREV_FRAME_TIME = 0
NEW_FRAME_TIME = 0

def FPS_Counter(frame):
    global PREV_FRAME_TIME, NEW_FRAME_TIME
    
    frame = cv2.resize(frame, (500, 300))
    font = cv2.FONT_HERSHEY_SIMPLEX
    NEW_FRAME_TIME = time.time()

    fps = 1/(NEW_FRAME_TIME - PREV_FRAME_TIME)

    PREV_FRAME_TIME = NEW_FRAME_TIME
    fps = int(fps)
    fps = str(fps)

    # (image, text, org[tuple for x and y], font type, scale, thickness, line type)
    cv2.putText(frame, fps, (7,35), font, 1, (100,255,0), 2, cv2.LINE_AA)
    return frame

def Get_Gesture(handLandmarks):
    # Get detected hand landmarks in array format
    landmarks = handLandmarks.landmark
    fingers = []

    # Check thumb based on difference in x positions (thumb points horizontally for open/closed hand)
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Check other fingers x positions (fingers point vertically for open/closed hand)
    tips = [8, 12, 16, 20]

    for tip in tips:
        if landmarks[tip].y < landmarks[tip-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    # Add up all fingers that are open/closed and check
    total = sum(fingers)
    if total == 5:
        return "OPEN"
    elif total == 0:
        return "CLOSED"
    else:
        return "OTHER"

def Get_Direction(handLandmarks):
    # Get landmark info for detected hand
    landmarks = handLandmarks.landmark

    # Get the base and tip of the index finger based on set array space
    base = landmarks[5]
    tip = landmarks[8]

    # Check which way the finger is pointing based on respective X and Y values
    delta_x = tip.x - base.x
    delta_y = tip.y - base.y

    # Based on difference between the tip and base of index, return respective direction
    if abs(delta_x) > abs(delta_y):
        # If there is a bigger change in the x values between tip/base, we are indicating horizontal direction
        if delta_x > 0:
            return "RIGHT"
        else:
            return "LEFT"
    else:
        if delta_y > 0:
            return "DOWN"
        else:
            return "UP"
        
