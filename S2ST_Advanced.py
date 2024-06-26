import speech_recognition as sr
import os
import deepl
import time
import requests

auth_key = ""  # DeepL Api key
translator = deepl.Translator(auth_key)

voice_id = "flq6f7yk4E4fJM5XTYuZ"  # Voice ID ElevanLabs
xi_api_key = "" # ElevanLabs api key

def speak_text(text, lang):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": xi_api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
    else:
        print("An error occurred while converting text to audio:", response.status_code)

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        print("Dinleniyor...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language='en-US') # Language spoken
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API request failed"
    except sr.UnknownValueError:
        response["error"] = "Voice unintelligible"

    return response

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    target_lang = "TR"  # You can change the target language here
    gtts_lang = "tr"  # You can change the target language here (lower)

    while True:
        input("Press a key to continue...")
        print("Waiting for your speech (say 'exit' to exit)")
        result = recognize_speech_from_mic(recognizer, microphone)

        if result["transcription"]:
            print(f"Defined text: {result['transcription']}")
            if "çık" in result["transcription"].lower():
                print("Exiting...")
                break

            start_time = time.time()  # Save start time

            # Translate text using Deepl API
            translated_result = translator.translate_text(result["transcription"], target_lang=target_lang)
            translated_text = translated_result.text
            print(f"Translated text: {translated_text}")

            # Vocalize translated text with ElevenLabs API and gTTS
            speak_text(translated_text, gtts_lang)
            
            os.system("start output.mp3")  # Play audio file

            end_time = time.time()  # Record end time
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.2f} saniye")

        elif result["error"]:
            print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()
