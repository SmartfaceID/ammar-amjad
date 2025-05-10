# -*- coding: utf-8 -*-
"""
Created on Fri May  9 23:17:06 2025

@author: Obaid
"""

import speech_recognition as sr
import pyttsx3
import time

# تهيئة مكتبة الصوت
engine = pyttsx3.init()

# دالة لتحويل النص إلى صوت
def speak(text):
    engine.say(text)
    engine.runAndWait()

# دالة لاكتشاف الكلمة المفتاحية "Hey System"
def listen_for_keyword():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("[INFO] Listening for 'Hi System'...")
    speak("أنا في وضع الاستماع. قل: Hi System")

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"[DEBUG] Detected command: {command}")
                if "hey system" in command:
                    speak("مرحبًا بك في نظام التحقق من بصمة الوجه. ما الذي تريد فعله؟")
                    return True
            except sr.WaitTimeoutError:
                print("[INFO] Timeout. لم يتم الكشف عن أي صوت.")
            except sr.UnknownValueError:
                print("[INFO] لم أتمكن من فهم الصوت.")
            except Exception as e:
                print(f"[ERROR] {str(e)}")

# دالة الاستماع للأوامر
def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    commands = {
        "login": "تسجيل الدخول",
        "verify face": "التحقق عن طريق الكاميرا",
        "train model": "تدريب النموذج",
        "add person": "إضافة شخص جديد"
    }

    while True:
        speak("ما الذي تريد فعله؟ يمكنك قول: تسجيل الدخول، التحقق عن طريق الكاميرا، تدريب النموذج، أو إضافة شخص جديد")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"[DEBUG] Detected command: {command}")

                for key, value in commands.items():
                    if key in command:
                        speak(f"تم اختيار {value}")
                        return key

                speak("لم أفهم الأمر. حاول مرة أخرى.")
            except sr.WaitTimeoutError:
                speak("لم أسمع أي أمر. هل تريد محاولة أخرى؟")
            except sr.UnknownValueError:
                speak("لم أتمكن من فهم الصوت. حاول مرة أخرى.")
            except Exception as e:
                print(f"[ERROR] {str(e)}")

# دالة تنفيذ الأوامر
def execute_command(command):
    if command == "login":
        speak("هل تريد تسجيل الدخول عن طريق اسم المستخدم أم الكاميرا؟")
    elif command == "verify face":
        speak("جاري التحقق من الوجه عن طريق الكاميرا...")
    elif command == "train model":
        speak("جاري تدريب النموذج...")
    elif command == "add person":
        speak("جاري إضافة شخص جديد للنظام...")
    else:
        speak("الأمر غير معروف. حاول مرة أخرى.")

if __name__ == "__main__":
    if listen_for_keyword():
        command = listen_for_commands()
        execute_command(command)
