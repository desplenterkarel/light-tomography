import numpy as np
import pyaudio
import time
from logger import LOGGER


class Microphone:
    def __init__(self):
        formatt = pyaudio.paInt16  # Audio format (16-bit PCM)
        channels = 1  # Mono audio
        rate = 44100  # Sample rate (samples per second)
        self.chunk = 1024  # Number of frames per buffer

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=formatt, channels=channels,
                                      rate=rate, input=True,
                                      frames_per_buffer=self.chunk)
        # WAIT, SHOULD THESE BE WRITTEN AS SELF? OR VARIABLES OUTSIDE CLASS?
        self.spike_counter = 0
        self.index = -1  # USEFUL, maybe TO BE REMOVED WHEN IMPLEMENTING TIME.SLEEP()
        self.intensities = []
        LOGGER.debug("Microphone Initialized")

    # this should be in a while True loop in another file
    def is_vibrating(self):
        data = self.stream.read(self.chunk, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        intensity = np.sqrt(np.mean(audio_data.astype(np.float32) ** 2))
        self.intensities.append(intensity)
        self.index += 1
        # time.sleep(0.001)  # Adjust the delay as needed

        if intensity > 800:
            self.spike_counter += 1
           # LOGGER.debug(f"Vibration pulse nr: {self.spike_counter} registered with intensity {intensity}")
            return True

        return False

    def get_pulse_number(self):
        return self.spike_counter

    def clean(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
