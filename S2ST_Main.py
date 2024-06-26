import queue
import os
import re
import sys
from google.cloud import speech
import pyaudio
import deepl
import requests
import pygame
import threading
import logging

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Initialize the DeepL translator
auth_key = "" # DeepL API key https://www.deepl.com/en/your-account/keys
translator = deepl.Translator(auth_key)

voice_id = "flq6f7yk4E4fJM5XTYuZ"  
xi_api_key = "" # ElevanLabs API key https://elevenlabs.io/app/speech-synthesis


class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate=RATE, chunk=CHUNK):
        """The audio -- and generator -- is guaranteed to be on the main thread."""
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        """Closes the stream, regardless of whether the connection was lost or not."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Generates audio chunks from the stream of audio data in chunks."""
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them."""
    num_chars_printed = 0

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()
            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)

            translation_result = translator.translate_text(transcript, target_lang="EN-US") # Çeviri Yapılacak dil
            translated_text = translation_result.text
            print("Translation:", translated_text)

            # Convert translated text to speech asynchronously
            threading.Thread(target=speak_text, args=(translated_text, "EN-US")).start()

            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0

    return transcript

def main():
    # Speech to Text Language
    language_code = "tr-TR"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        listen_print_loop(responses)


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
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("output.mp3", "wb") as f:
                f.write(response.content)
            
            pygame.init()
            pygame.mixer.init()
            
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)  # Adjust as needed

        else:
            logging.error(f"Error converting text to speech: {response.status_code}")
            print("Metin sese dönüştürülürken bir hata oluştu:", response.status_code)

    except Exception as e:
        logging.error(f"Error during text to speech conversion: {str(e)}")
        print("Metin sese dönüştürülürken bir hata oluştu:", str(e))

    finally:
        pygame.mixer.quit()
        pygame.quit()

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    main()