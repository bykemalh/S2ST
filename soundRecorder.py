import sounddevice as sd
import wavio
import numpy as np
import threading

# Ses parametreleri
samplerate = 44100  # Örnekleme hızı
channels = 2  # Stereo
dtype = 'int16'  # Veri tipi

# Kaydetme durumu için bir bayrak ve kayıt verilerini saklamak için bir liste
recording = False
recorded_frames = []

def callback(indata, frames, time, status):
    if recording:
        recorded_frames.append(indata.copy())

def start_recording():
    global recording
    recording = True
    with sd.InputStream(samplerate=samplerate, channels=channels, dtype=dtype, callback=callback):
        while recording:
            sd.sleep(1000)  # 1 saniye bekle

def stop_recording():
    global recording
    recording = False

def save_recording(filename="output.wav"):
    # Kayıtlı verileri numpy dizisi olarak birleştir
    np_frames = np.concatenate(recorded_frames, axis=0)
    wavio.write(filename, np_frames, samplerate, sampwidth=2)

def main():
    print("Kaydı başlatmak için Enter tuşuna basın...")
    input()
    print("Kayıt başladı... Durdurmak için Enter tuşuna basın...")
    
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()
    
    input()
    stop_recording()
    recording_thread.join()
    
    save_recording()
    print("Kayıt 'output.wav' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
