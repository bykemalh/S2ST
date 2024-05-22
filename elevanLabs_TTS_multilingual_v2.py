import requests

def convert_text_to_speech(text, voice_id, xi_api_key):
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
        "use_speaker_boost": True,
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        with open('output.mp3', 'wb') as f:
            f.write(response.content)
        print("Succes : output.mp3")
    else:
        print("Error !")

# User Setting
text_to_convert = "Merhaba ben Kemal Hafızoğlu , Sakarya Uygulamalı Bilimler Ünüversitesi Ögrencisiyim ."
voice_id = "flq6f7yk4E4fJM5XTYuZ" # Voice ID 
xi_api_key = "" # ElevanLabs api key buraya giriniz !

# Text to Speech function run 
convert_text_to_speech(text_to_convert, voice_id, xi_api_key)
