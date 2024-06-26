# Speech-to-Speech Translator

This project uses Google Cloud Speech-to-Text API to transcribe speech to text, DeepL API to translate the transcribed text, and ElevenLabs API to convert the translated text back to speech. This creates a seamless speech-to-speech translation system.

## Prerequisites

Before running this project, ensure you have the following dependencies installed:

- Python 3.7 or later
- Google Cloud SDK (gcloud)
- Pyaudio
- Requests
- Pygame
- DeepL API key
- ElevenLabs API key

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/bykemalh/S2ST.git
    cd S2ST
    ```

2. **Set up a virtual environment:**
    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required Python packages:**
    ```sh
    pip install google-cloud-speech pyaudio deepl requests pygame
    ```

4. **Install Google Cloud SDK:**
    Follow the installation instructions for your operating system [here](https://cloud.google.com/sdk/docs/install).

5. **Authenticate with Google Cloud:**
    ```sh
    gcloud auth login
    gcloud auth application-default login
    ```

6. **Enable the Google Cloud Speech-to-Text API:**
    ```sh
    gcloud services enable speech.googleapis.com
    ```

7. **Set up API keys:**
    Replace the placeholder values in the script with your actual DeepL and ElevenLabs API keys.
    ```python
    auth_key = "your-deepl-auth-key"
    xi_api_key = "your-elevenlabs-api-key"
    ```

## Running the Application

To run the application, simply execute the `main.py` script:

```sh
python S2ST_NewAdvanced.py
```

## How It Works

1. **Audio Input:**
    - The application opens a microphone stream using the `pyaudio` library and captures audio in real-time.

2. **Speech-to-Text:**
    - The captured audio is sent to the Google Cloud Speech-to-Text API, which returns the transcribed text.

3. **Translation:**
    - The transcribed text is translated to English using the DeepL API.

4. **Text-to-Speech:**
    - The translated text is sent to the ElevenLabs API, which converts it to speech and plays it back.

## Dependencies

Ensure you have the following libraries installed:

- `google-cloud-speech`
- `pyaudio`
- `deepl`
- `requests`
- `pygame`

You can install these dependencies using the following command:

```sh
pip install google-cloud-speech pyaudio deepl requests pygame
```

## Configuration

Modify the following variables in the script to match your settings:

- `auth_key`: Your DeepL API key.
- `xi_api_key`: Your ElevenLabs API key.
- `voice_id`: The voice ID to be used with ElevenLabs API.
- `RATE`: The audio sample rate (default is 16000).
- `CHUNK`: The audio chunk size (default is 1600).

## Logging

Logging is set up in the script to capture errors during the text-to-speech conversion process. You can enable more detailed logging by uncommenting the logging configuration line.

```python
# logging.basicConfig(level=logging.DEBUG)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you wish to contribute to this project, please fork the repository and create a pull request.

## Acknowledgments

- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/docs)
- [DeepL API](https://www.deepl.com/docs-api)
- [ElevenLabs API](https://www.elevenlabs.io/docs/api)


<hr>

### Developed By

This algorithm was developed by Kemal Hafızoğlu.