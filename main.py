import numpy as np
import pyaudio
import pygame
import time


from modules.oscillator import Oscillator
from modules.modulator import Modulator
from modules.amplifier import Amplifier
from modules.filter import Filter
from modules.envelope import Envelope
from modules.MIDI import MIDI
from modules.ARP import ARP

FREQ_SAMPLE = 44100
SAMPLE_SIZE = 512

pygame.init()

oscillator = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)
modulator = Modulator(FREQ_SAMPLE, SAMPLE_SIZE)
amplifier = Amplifier(FREQ_SAMPLE, SAMPLE_SIZE)
envelope = Envelope(FREQ_SAMPLE, SAMPLE_SIZE)
filter = Filter(FREQ_SAMPLE, SAMPLE_SIZE)

note = 0
gate = False
trigger = False
cutoff = 0.5  # 0-1 but log scale from 20 Hz to 20 kHz

flag = pyaudio.paContinue


times = []

# with sample rate of 44.1kHz and 576 samples per callback, each invoation of
# the callback must take < 0.0131s.
def callback(in_data, frame_count, time_info, status_flags):
  start = time.time()

  global note, gate, trigger, flag
  # pitch, gate, trigger, velocity = arp.process(frame_count)

  # low_out_data = modulator.process(t, frame_count)
  # oscillator.set_input('wave', np.ones((SAMPLE_SIZE,)) * 0)
  oscillator.set_input('note', np.ones((SAMPLE_SIZE,)) * note)
  oscillator.process()
  out_data = oscillator.get_output('out_data')

  envelope.set_input('gate', np.ones((SAMPLE_SIZE,)) if gate else np.zeros((SAMPLE_SIZE,)))
  envelope.set_input('trigger', np.array([1] + [0] * (SAMPLE_SIZE - 1)) if trigger else np.zeros((SAMPLE_SIZE,)))
  envelope.process()
  env = envelope.get_output('env')

  amplifier.set_input('vol_mod', env)
  amplifier.set_input('in_data', out_data)
  amplifier.process()
  out_data = amplifier.get_output('out_data')

  filter._param['freq_cut'] = 20 * 10 ** (2 * cutoff)
  filter.set_input('freq_cut_mod', env)
  filter.set_input('in_data', out_data)
  filter.process()
  out_data = filter.get_output('out_data')

  trigger = False




  # out_data = filter.process(
  #   frame_count,
  #   out_data,
  #   20 * 10 ** (2 * cutoff) * np.ones((frame_count,)),
  #   env_data,
  #   0.5,
  # )

  end = time.time()
  times.append(end - start)
  if len(times) == 100:
    print(np.max(times))
    times.clear()

  return out_data.astype(np.float32).tobytes(), flag

# y scroll is pitch wheel
# x scroll is mod wheel
# pitch wheel is for changing pitch of osc
# modulation wheel determines how much modulation is applied to the filter cutoff, pitch of osc, and width of pulse
# glide is time variable TODO: legato
#

screen_width = 100
screen_height = 100
screen = pygame.display.set_mode((screen_width, screen_height))

lookup = {
  pygame.K_z: 48,  # C
  pygame.K_s: 49,  # C#
  pygame.K_x: 50,  # D
  pygame.K_d: 51,  # D#
  pygame.K_c: 52,  # E
  pygame.K_v: 53,  # F
  pygame.K_g: 54,  # F#
  pygame.K_b: 55,  # G
  pygame.K_h: 56,  # G#
  pygame.K_n: 57,  # A
  pygame.K_j: 58,  # A#
  pygame.K_m: 59,  # B
  pygame.K_COMMA: 60,  # C
}

lookup = {
  pygame.K_z: 36,  # C
  pygame.K_s: 37,  # C#
  pygame.K_x: 38,  # D
  pygame.K_d: 39,  # D#
  pygame.K_c: 40,  # E
  pygame.K_v: 41,  # F
  pygame.K_g: 42,  # F#
  pygame.K_b: 43,  # G
  pygame.K_h: 44,  # G#
  pygame.K_n: 45,  # A
  pygame.K_j: 46,  # A#
  pygame.K_m: 47,  # B
  pygame.K_COMMA: 48,  # C
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

# Initialize PyAudio
p = pyaudio.PyAudio()

stream = p.open(
  format=pyaudio.paFloat32,
  channels=1,
  rate=FREQ_SAMPLE,
  frames_per_buffer=SAMPLE_SIZE,
  output=True,
  stream_callback=callback,
)

stream.start_stream()

while stream.is_active() and flag == pyaudio.paContinue:
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      flag = pyaudio.paComplete

    # Check for key pressed
    if event.type == pygame.KEYDOWN and event.key in lookup:
      gate = True
      trigger = True
      note = lookup[event.key]
    elif event.type == pygame.KEYUP:
      if not sum(pygame.key.get_pressed()):
        gate = False
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
