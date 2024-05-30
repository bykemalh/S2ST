# Speech to Speech Translation

This Python project provides functionality for real-time speech-to-speech translation using two different methods. It utilizes speech recognition, translation, and text-to-speech libraries to enable translation between different languages.

## Features

- **Two Translation Methods:** Two different approaches for speech translation are implemented.
- **Real-time Translation:** The application translates speech input into the desired target language in real-time.
- **User Interaction:** User-friendly interface with instructions for interaction.
- **Flexibility:** Easily change target languages and adjust settings according to user requirements.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/bykemalh/S2ST.git
    ```

2. Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have valid API keys for the translation services used in the code.

## Usage

1. Run the script `speech_translation.py` using Python:

    ```bash
    python speech_translation.py
    ```

2. Follow the on-screen instructions to interact with the application:
   - Press any key to initiate speech recognition.
   - Speak into the microphone.
   - Wait for the translation and listen to the output.
   - Say "exit" to quit the application.

## Method 1: Using ElevenLabs and DeepL APIs

This method utilizes ElevenLabs API for text-to-speech conversion and DeepL API for translation. The translated text is then vocalized using the text-to-speech service.

### Requirements

- [ElevenLabs API Key]([https://www.eleven-labs.com/en/products/text-to-speech])
- [DeepL API Key](https://www.deepl.com/pro)

## Method 2: Using gTTS and Google Speech Recognition

This method employs Google Text-to-Speech (gTTS) for text-to-speech conversion and Google Speech Recognition for speech-to-text conversion. The translated text is then vocalized using gTTS.

### Requirements

- [Google Text-to-Speech (gTTS)](https://pypi.org/project/gTTS/)
- [Google Speech Recognition](https://pypi.org/project/SpeechRecognition/)

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE) file for details.

## Credits

- **Author:** [Your Name](https://github.com/bykemalh)
