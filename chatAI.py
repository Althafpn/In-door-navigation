from datetime import datetime
import pyttsx3
from gtts import gTTS
import pygame
import speech_recognition as sr
import os
from pydub import AudioSegment
import io
import google.generativeai as genai
import sounddevice
import data_1 
#Initializing
r=sr.Recognizer()  
activation_words = ['jake','hi','jack','giant','hey jake','hello jake','ok jake','hello white','hello boy'] #activation key, like Hey, Google
#API Connection
genai.configure(api_key='AIzaSyCgiH3gZ-4c6LzX36AvbMTIuTEFFvOvjDM')
#Text to speech
def speak(text, rate = 120): #function for system to speak to user.
    tts = gTTS(text = text, lang = 'en', tld='us')
    tts.save("temp.mp3") #save recorded audio
    pygame.mixer.init()
    sound = pygame.mixer.Sound("temp.mp3")
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    pygame.time.delay(int(sound.get_length() * 1000)) 
    pygame.mixer.stop()
    pygame.quit()
    os.remove("temp.mp3") #delete audio file after speech to text

#Recognise speech to text
def parseCommand(): #convert useful queries to meaningfull commands and use api to get necessary output
    print("Listening to command...")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=.5)
        r.pause_threshold = 1.5
        #listener.energy_threshold = 4000  # Adjust this value as needed
        r.dynamic_energy_threshold = True
        r.operation_timeout = 5 # Set the timeout to 10 seconds
        input_speech =r.listen(source)
        try:
            print("Recognizing speech")
            query = r.recognize_google(input_speech, language='en_us') #convert audio data to queries
            print(f'The input speech was: {query}')
            audio_data = input_speech.get_wav_data()
            audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
            now = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
            audio_segment.export("Listened audio_%s.wav" % now,format = 'wav') #save audio file with date
        except Exception as exception:
            print('I did not quiet catch that...')
            speak('I did not quiet catch that...')
            return None
    return query

def geminiAi(query):
    print("Gemini Activated")
    speak("please wait")
    data_1.fetch_result(query)
    response = data_1.result
    # Extract the generated content from the response
    generated_text = response.candidates[0].content.parts[0].text
    # Process the generated text if needed (e.g., remove unnecessary parts)
    processed_text = generated_text[:500] # Limiting to first 500 characters for simplicity
    processed_text = processed_text.replace('*','')
    # Convert the processed text to speech
    print(processed_text)
    return processed_text
#Exit process
def exitAI():
    print('exiting')
    speak('Good bye')
flag = False
print(__name__)
#Main Loop
#Check is the program is running as main

if __name__ == '__main__':
    speak('I am R2D2 how can i help you')

    while True:
        activation_detected = False
        query = parseCommand()
        if query == None:
            print("No speech detected, Try again") 
            continue
        else:
            query = query.lower().split()
        print(query)

        for word in activation_words:
            if word in query:
                print("Activation Key: ",word)
                print(query[0])
                query.pop(0)
                print("Processed Query: ",query)
                activation_detected = True
                break
           
        if activation_detected:
            #Gemini AI Result
            # if activation_detected:
                # Process the query to remove 'say' and activate Gemini AI
                query_text = ' '.join(query)
                AIResult = geminiAi(query_text)
                speak(AIResult)
        #To Exit        
        if query[0] == 'exit':
                exitAI()
                break

