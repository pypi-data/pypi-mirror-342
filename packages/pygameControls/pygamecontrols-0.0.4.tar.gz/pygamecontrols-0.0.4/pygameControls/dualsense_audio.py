import os
import time
import numpy as np
import sounddevice as sd
import alsaaudio
import pulsectl

class DualSenseAudio:
    def __init__(self):
        self.alsa_devices = self._get_alsa_devices()
        self.pulse_devices = self._get_pulseaudio_devices()
        self.dualsense_device = self._detect_dualsense()

    def _get_alsa_devices(self):
        try:
            cards = alsaaudio.cards()
            return cards
        except Exception as e:
            print("ALSA detection failed:", e)
            return []

    def _get_pulseaudio_devices(self):
        try:
            pulse = pulsectl.Pulse("dualsense-audio")
            sinks = pulse.sink_list()
            return sinks
        except Exception as e:
            print("PulseAudio detection failed:", e)
            return []

    def _detect_dualsense(self):
        # Check ALSA names
        for card in self.alsa_devices:
            if "DualSense" in card:
                return {'type': 'alsa', 'name': card}

        # Check PulseAudio sinks
        for sink in self.pulse_devices:
            if "dualsense" in sink.description.lower():
                return {'type': 'pulse', 'name': sink.name}

        return None

    def play_tone(self, frequency=440.0, duration=2.0, volume=0.5):
        if not self.dualsense_device:
            print("DualSense speaker not found.")
            return

        print(f"Playing tone on DualSense ({self.dualsense_device['type']})...")

        fs = 48000  # Sample rate
        t = np.linspace(0, duration, int(fs * duration), False)
        tone = np.sin(frequency * 2 * np.pi * t) * volume
        audio = tone.astype(np.float32)

        if self.dualsense_device['type'] == 'pulse':
            sd.play(audio, samplerate=fs, device=self.dualsense_device['name'])
        elif self.dualsense_device['type'] == 'alsa':
            device_index = self.alsa_devices.index(self.dualsense_device['name'])
            sd.play(audio, samplerate=fs, device=device_index)
        sd.wait()

    def list_devices(self):
        print("ALSA Devices:")
        for card in self.alsa_devices:
            print(f" - {card}")
        print("\nPulseAudio Devices:")
        for sink in self.pulse_devices:
            print(f" - {sink.name} ({sink.description})")

