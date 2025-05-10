import os
import cv2
from deepface import DeepFace

def verify_face():
    print("[+] Choose an image to verify...")

    # Ask the user for the image path
    img_path = input("Enter the image path for verification: ")

    if not os.path.exists(img_path):
        print("[!] The path is incorrect. Please try again.")
        return

    # Perform the identity verification
    try:
        result = DeepFace.find(img_path=img_path, db_path="dataset", enforce_detection=True)
        if len(result) > 0:
            print("[✓] The person was identified!")
            print(result[0].identity.values[0])
        else:
            print("[!] No match found.")
    except Exception as e:
        print(f"[!] Verification failed: {e}")

if __name__ == "__main__":
    verify_face()