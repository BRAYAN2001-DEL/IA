import speech_recognition as sr
import pyttsx3

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
#for voice in voices:
   # print(voice)


engine.say("Buenos dias Brayan Steeven Salmon Barzola Soy tu Asistente virtual Personal En que te puedo Ayudar")

engine.runAndWait()

try:
    with sr.Microphone() as source:
        print("Escuchando....")
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
        rec = listener.recognize_google(voice)
        rec = rec.lower()
       # if name in rec:
           # rec = rec.replace(name, "")
        print(rec)
except:
    pass