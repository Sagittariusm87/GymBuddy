
import cv2 as cv
import numpy as np
import body_detection_module as bd

mybody = bd.BodyDetector(min_det_con=0.9)
pushupcount = 0
up = False
minangle = 0

def analyze_frame(img):
    global pushupcount, up, minangle

    feedback = {"message": "", "count": pushupcount}

    mybody.findbodies(img)
    lmlist = mybody.getcoords(img)
    if len(lmlist) < 29:
        feedback["message"] = "No full body detected"
        return feedback

    right_shoulder, right_elbow, right_wrist = 12, 14, 16
    left_shoulder, left_elbow, left_wrist = 11, 13, 15
    right_hip, right_ankle = 24, 28

    right_arm_angle = mybody.getangle(right_shoulder, right_elbow, right_wrist)
    left_arm_angle = mybody.getangle(left_shoulder, left_elbow, left_wrist)
    body_alignment = mybody.getangle(right_shoulder, right_hip, right_ankle)

    arm_angle = min(right_arm_angle, left_arm_angle)
    prevstate = up

    if prevstate != up and prevstate == False:
        minangle = arm_angle
    if prevstate != up and prevstate == True:
        maxangle = arm_angle
        pushupcount += 1

    if arm_angle < 60:
        up = True
    if arm_angle > 150:
        up = False

    if up:
        feedback["message"] = "Go High"
    else:
        feedback["message"] = "Go Lower!"

    if body_alignment < 160:
        feedback["message"] += " | Keep your body straight!"

    feedback["count"] = pushupcount
    feedback["elbow_angle"] = arm_angle
    feedback["alignment"] = body_alignment

    return feedback
