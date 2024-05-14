import numpy as np
import pyaudio
import pygame
import time

from modules.VCO import VCO
from modules.MIDI import MIDI

SAMPLE_RATE = 44100

vco = VCO(SAMPLE_RATE)
midi = MIDI()

voltage = 0

def callback(in_data, frame_count, time_info, status_flags):
    global t, voltage
    out_data = vco.process(t, frame_count, voltage)
    # print(time_info)
    t += frame_count
    return out_data.tobytes(), pyaudio.paContinue

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
      }


stream.start_stream()

while stream.is_active():
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      raise KeyError()

    # Check for key pressed
    if event.type == pygame.KEYDOWN and event.key in lookup:
      note = lookup[event.key]
      voltage = midi.note_to_cv(note)
      


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
