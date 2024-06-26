import speech_recognition as sr
from gtts import gTTS
import os
import deepl
import time

# Deepl API key
auth_key = ""
translator = deepl.Translator(auth_key)

def speak_text(text, lang):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows. You can use 'afplay' on MacOS and 'mpg321' on Linux.

def recognize_speech_from_mic(recognizer, microphone):
    """Recognize speech from the microphone and convert it to text."""
    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language='tr-TR') # Spoken language
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API request failed"
    except sr.UnknownValueError:
        response["error"] = "Speech not understood"

    return response

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    target_lang = "RU"  # You can change the target language from here
    gtts_lang = "ru"  # Target language for gTTS

    while True:
        input("Press any key to continue...")
        print("Listening for your speech (say 'exit' to quit)...")
        result = recognize_speech_from_mic(recognizer, microphone)

        if result["transcription"]:
            print(f"Recognized text: {result['transcription']}")
            if "exit" in result["transcription"].lower():
                print("Exiting...")
                break
            
            start_time = time.time()  # Record start time

            # Translate the text using Deepl API
            translated_result = translator.translate_text(result["transcription"], target_lang=target_lang)
            translated_text = translated_result.text
            print(f"Translated text: {translated_text}")

            # Convert the translated text to speech using gTTS
            speak_text(translated_text, gtts_lang)

            end_time = time.time()  # Record end time
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.2f} seconds")

        elif result["error"]:
            print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()
