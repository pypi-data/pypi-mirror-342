import time
import threading
import numpy as np
import sounddevice as sd
import alsaaudio
import pulsectl
from pydualsense import *


class DualSenseEdgeController:
    def __init__(self):
        # DualSense input/output interface
        self.ds = pydualsense()
        self.ds.init()
        self._listening = False
        self._bindings = {}

        # Audio detection
        self.alsa_devices = self._get_alsa_devices()
        self.pulse_devices = self._get_pulseaudio_devices()
        self.dualsense_audio_device = self._detect_dualsense_audio()

        print("DualSense initialized.")

    # ---------------------- Device Controls ----------------------

    def set_rumble(self, small_motor: int, big_motor: int):
        self.ds.setRumble(small_motor, big_motor)

    def stop_rumble(self):
        self.set_rumble(0, 0)

    def set_led_color(self, r: int, g: int, b: int):
        self.ds.setLightBarColor(r, g, b)

    def set_trigger_effects(self, left_mode='Off', right_mode='Off', force=0):
        left = getattr(TriggerModes, left_mode.upper(), TriggerModes.Off)
        right = getattr(TriggerModes, right_mode.upper(), TriggerModes.Off)
        self.ds.triggerL.setMode(left)
        self.ds.triggerR.setMode(right)
        if force > 0:
            self.ds.triggerL.setForce(force)
            self.ds.triggerR.setForce(force)

    # ---------------------- Predefined Rumble Patterns ----------------------

    def rumble_pattern(self, pattern: str, duration: float = 1.0):
        patterns = {
            "pulse": self._pulse_rumble,
            "heartbeat": self._heartbeat_rumble,
            "buzz": self._buzz_rumble,
            "wave": self._wave_rumble,
            "alarm": self._alarm_rumble,
        }
        if pattern in patterns:
            threading.Thread(target=patterns[pattern], args=(duration,), daemon=True).start()
        else:
            print(f"Unknown rumble pattern: {pattern}")

    def _pulse_rumble(self, duration):
        end = time.time() + duration
        while time.time() < end:
            self.set_rumble(50, 150)
            time.sleep(0.2)
            self.stop_rumble()
            time.sleep(0.2)

    def _heartbeat_rumble(self, duration):
        end = time.time() + duration
        while time.time() < end:
            self.set_rumble(200, 200)
            time.sleep(0.1)
            self.stop_rumble()
            time.sleep(0.1)
            self.set_rumble(100, 100)
            time.sleep(0.1)
            self.stop_rumble()
            time.sleep(0.4)

    def _buzz_rumble(self, duration):
        self.set_rumble(80, 255)
        time.sleep(duration)
        self.stop_rumble()

    def _wave_rumble(self, duration):
        start = time.time()
        while time.time() - start < duration:
            for i in range(0, 256, 25):
                self.set_rumble(i, 255 - i)
                time.sleep(0.05)
            for i in reversed(range(0, 256, 25)):
                self.set_rumble(i, 255 - i)
                time.sleep(0.05)
        self.stop_rumble()

    def _alarm_rumble(self, duration):
        end = time.time() + duration
        while time.time() < end:
            self.set_rumble(255, 0)
            time.sleep(0.1)
            self.set_rumble(0, 255)
            time.sleep(0.1)
        self.stop_rumble()

    # ---------------------- Input Listener + Bindings ----------------------

    def bind(self, button: str, action: callable):
        """Bind a button to a callable. Ex: controller.bind('cross', lambda: rumble_pattern('buzz'))"""
        self._bindings[button] = action

    def start_input_listener(self):
        def listen():
            while self._listening:
                #self.ds.update()
                for button, action in self._bindings.items():
                    if getattr(self.ds, button, False):
                        action()
        self._listening = True
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def stop_input_listener(self):
        self._listening = False

    # ---------------------- Audio Output ----------------------

    def _get_alsa_devices(self):
        try:
            return alsaaudio.cards()
        except Exception:
            return []

    def _get_pulseaudio_devices(self):
        try:
            pulse = pulsectl.Pulse("dualsense-audio")
            return pulse.sink_list()
        except Exception:
            return []

    def _detect_dualsense_audio(self):
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
        if not self.dualsense_audio_device:
            print("DualSense speaker not detected.")
            return

        print(f"Playing tone on DualSense ({self.dualsense_audio_device['type']})...")

        fs = 48000  # Sample rate
        t = np.linspace(0, duration, int(fs * duration), False)
        tone = np.sin(frequency * 2 * np.pi * t) * volume
        audio = tone.astype(np.float32)

        try:
            if self.dualsense_audio_device['type'] == 'pulse':
                sd.play(audio, samplerate=fs, device=self.dualsense_audio_device['name'])
            elif self.dualsense_audio_device['type'] == 'alsa':
                device_index = self.alsa_devices.index(self.dualsense_audio_device['name'])
                sd.play(audio, samplerate=fs, device=device_index)
            sd.wait()
        except Exception as e:
            print("Failed to play tone:", e)

    def list_audio_devices(self):
        print("ALSA Devices:")
        for card in self.alsa_devices:
            print(f" - {card}")
        print("\nPulseAudio Devices:")
        for sink in self.pulse_devices:
            print(f" - {sink.name} ({sink.description})")

    # ---------------------- Cleanup ----------------------

    def close(self):
        self.ds.close()

if __name__ == "__main__":
    
    controller = DualSenseController()

    # Bind buttons to patterns
    controller.bind("cross", lambda: controller.rumble_pattern("heartbeat", 1.5))
    controller.bind("circle", lambda: controller.rumble_pattern("buzz", 0.5))
    controller.bind("triangle", lambda: controller.rumble_pattern("pulse", 2))
    controller.bind("square", lambda: controller.set_led_color(255, 0, 0))

    # Start listening
    controller.start_input_listener()
