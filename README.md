                                    ================== READ ME INFORMATION ==================

1. This code utilizes mediapipe version 0.10.21 specifically due to the use of 'MP.solutions.hands'
    - To download the respective library (python -m pip install mediapipe==0.10.21)
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
    - Separate functions into specific modules/classes
    - Create detection feature for hand signals
    - Create simple game
    - Translate motion controls into game
