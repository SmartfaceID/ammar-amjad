# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 20:29:55 2025

@author: Obaid
"""

import cv2
import os
import numpy as np
import datetime

def circular_crop(img, size=300):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    radius = min(center[0], center[1], size // 2)

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)

    circular_img = cv2.bitwise_and(img, img, mask=mask)
    return circular_img

def add_new_person_to_dataset():
    # طلب اسم الشخص
    person_name = input("[+] Enter the name of the person: ")

    # التحقق إذا كان اسم الشخص فارغ أو لا
    if not person_name.strip():
        print("[!] Name cannot be empty. Exiting...")
        return

    # إنشاء مجلد للشخص في dataset إذا لم يكن موجود
    dataset_dir = "dataset"
    person_dir = os.path.join(dataset_dir, person_name)
    os.makedirs(person_dir, exist_ok=True)

    print(f"[+] Starting the camera for {person_name}...")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Could not open the camera.")
        return

    image_count = 0
    while image_count < 20:  # نلتقط 20 صور للشخص
        ret, frame = cap.read()
        if not ret:
            print("[!] Failed to grab frame.")
            break

        # عرض الصورة الدائرية للحظات فقط
        frame_resized = cv2.resize(frame, (300, 300))
        circ_frame = circular_crop(frame_resized)

        black_bg = np.zeros((400, 400, 3), dtype=np.uint8)
        x_offset = (400 - circ_frame.shape[1]) // 2
        y_offset = (400 - circ_frame.shape[0]) // 2
        black_bg[y_offset:y_offset+circ_frame.shape[0], x_offset:x_offset+circ_frame.shape[1]] = circ_frame

        cv2.imshow("Capturing Face...", black_bg)
        cv2.waitKey(1000)  # عرض الصورة لمدة ثانية واحدة

        # حفظ الصورة داخل مجلد الشخص
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        image_path = os.path.join(person_dir, f"{timestamp}_{image_count+1}.jpg")
        cv2.imwrite(image_path, frame)

        print(f"[+] Image {image_count+1} saved at: {image_path}")
        image_count += 1

    cap.release()
    cv2.destroyAllWindows()

    print(f"[+] {image_count} images saved for {person_name} in dataset.")
