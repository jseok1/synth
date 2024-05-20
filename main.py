import numpy as np
import pyaudio
import pygame
import time


from modules.VCO import VCO
from modules.LFO import LFO
from modules.VCA import VCA
from modules.VCF import VCF
from modules.ADSR import ADSR
from modules.MIDI import MIDI

SAMPLE_RATE = 44100

oscillator = VCO(SAMPLE_RATE)
low_oscillator = LFO(SAMPLE_RATE)
amplifier = VCA(SAMPLE_RATE)
envelope = ADSR(SAMPLE_RATE)
filter = VCF(SAMPLE_RATE)

midi = MIDI()

voltage = 0
pressing = False
cutoff = 0.5 # 0-1 but log scale from 20 Hz to 20 kHz

# with sample rate of 44.1kHz and 576 samples per callback, each invoation of
# the callback must take < 0.0131s.
def callback(in_data, frame_count, time_info, status_flags):
    t0 = time.time()

    global t, voltage
    low_data = low_oscillator.process(t, frame_count)
    out_data = oscillator.process(t, frame_count, voltage, low_data)
    env_data = envelope.process(t,
                                frame_count,
                                np.ones(frame_count) if pressing else np.zeros(frame_count),
                                attack=np.ones(frame_count) * 0.1,
                                decay=np.ones(frame_count) * 0.2,
                                sustain=np.ones(frame_count) * 0.75,
                                release=np.ones(frame_count) * 0.2)
    out_data = amplifier.process(out_data, 0.1 * env_data)
    out_data = filter.process(frame_count, out_data, 20 * 10 ** (3 * cutoff), 5.0)

    # print(time_info)
    t += frame_count

    t1 = time.time()
    # print(t1 - t0)
    return out_data.astype(np.float32).tobytes(), pyaudio.paContinue

# Initialize PyAudio
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                output=True,
                stream_callback=callback)

t = 0

import pygame

# Initialize pygame
pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

lookup = {
        pygame.K_z: 48, # C
        pygame.K_s: 49, # C#
        pygame.K_x: 50, # D
        pygame.K_d: 51, # D#
        pygame.K_c: 52, # E
        pygame.K_v: 53, # F
        pygame.K_g: 54, # F#
        pygame.K_b: 55, # G
        pygame.K_h: 56, # G#
        pygame.K_n: 57, # A
        pygame.K_j: 58, # A#
        pygame.K_m: 59, # B
        pygame.K_COMMA: 60, # C
      }

lookup = {
        pygame.K_z: 36, # C
        pygame.K_s: 37, # C#
        pygame.K_x: 38, # D
        pygame.K_d: 39, # D#
        pygame.K_c: 40, # E
        pygame.K_v: 41, # F
        pygame.K_g: 42, # F#
        pygame.K_b: 43, # G
        pygame.K_h: 44, # G#
        pygame.K_n: 45, # A
        pygame.K_j: 46, # A#
        pygame.K_m: 47, # B
        pygame.K_COMMA: 48, # C
      }


# lookup = {
#         pygame.K_z: 24, # C
#         pygame.K_s: 25, # C#
#         pygame.K_x: 26, # D
#         pygame.K_d: 27, # D#
#         pygame.K_c: 28, # E
#         pygame.K_v: 29, # F
#         pygame.K_g: 30, # F#
#         pygame.K_b: 31, # G
#         pygame.K_h: 32, # G#
#         pygame.K_n: 33, # A
#         pygame.K_j: 34, # A#
#         pygame.K_m: 35, # B
#         pygame.K_COMMA: 36, # C
#       }


stream.start_stream()

while stream.is_active():
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      raise KeyError()

    # Check for key pressed
    if event.type == pygame.KEYDOWN and event.key in lookup:
      pressing = True
      note = lookup[event.key]
      voltage = midi.note_to_cv(note)
    elif event.type == pygame.KEYUP:
      if not sum(pygame.key.get_pressed()):
        pressing = False
    elif event.type == pygame.MOUSEWHEEL:
      if event.y == 1:
        cutoff = min(cutoff + 0.1, 1.0)
      else:
        cutoff = max(cutoff - 0.1, 0.0)
      print(f'{cutoff:.3f}')

  # Update the display
  pygame.display.flip()

  # Cap the frame rate
  pygame.time.Clock().tick(60)

pygame.quit()

stream.stop_stream()
stream.close()

p.terminate()


# idea: pass around buffer through modules until output
# but need history?
