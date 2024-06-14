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
from modules.arpeggiator import Arpeggiator
from modules.mixer import Mixer

FREQ_SAMPLE = 44100
SAMPLE_SIZE = 256

pygame.init()

oscillator = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)
oscillator2 = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)
modulator = Modulator(FREQ_SAMPLE, SAMPLE_SIZE)
amplifier = Amplifier(FREQ_SAMPLE, SAMPLE_SIZE)
envelope = Envelope(FREQ_SAMPLE, SAMPLE_SIZE)
filter = Filter(FREQ_SAMPLE, SAMPLE_SIZE)
arpeggiator = Arpeggiator(FREQ_SAMPLE, SAMPLE_SIZE)
mixer = Mixer(FREQ_SAMPLE, SAMPLE_SIZE)

key = 0
keys = []
clear = False
gate = False
trigger = False
freq_cut = 0.5  # 0-1 but log scale from 20 Hz to 20 kHz
res = 1 / np.sqrt(2)

flag = pyaudio.paContinue


times = []

# with sample rate of 44.1kHz and 512 samples per callback, each invoation of
# the callback must take < 0.0116s. 0.0058 at 256 samples.
def callback(in_data, frame_count, time_info, status_flags):
  start = time.time()

  global key, gate, trigger
  notes = np.array([lookup[key] for key in keys])
  if False:
    note = lookup[key]
    oscillator.set_input('note', np.ones((SAMPLE_SIZE,)) * note)
    oscillator.process()
    out_data = oscillator.get_output('out_data')

    envelope.set_input('gate', np.ones((SAMPLE_SIZE,)) if gate else np.zeros((SAMPLE_SIZE,)))
    envelope.set_input('trigger', np.array([1] + [0] * (SAMPLE_SIZE - 1)) if trigger else np.zeros((SAMPLE_SIZE,)))
    envelope.process()
    env = envelope.get_output('env')
  
  note = np.zeros((SAMPLE_SIZE,))  
  gate = np.zeros((SAMPLE_SIZE,))  
  trigger = np.zeros((SAMPLE_SIZE,))  

  if notes.size:
    arpeggiator._param['notes'] = notes
    arpeggiator.process()
    note = arpeggiator.get_output('note')
    gate = arpeggiator.get_output('gate')
    trigger = arpeggiator.get_output('trigger')

  oscillator.set_input('note', np.ones((SAMPLE_SIZE,)) * note)
  oscillator.process()
  mixer.set_input('in_data_1', oscillator.get_output('out_data'))
  

  oscillator2._param['wave'] = 1
  oscillator2._param['freq'] = 8.175799 * 2**4
  oscillator2.set_input('note', np.ones((SAMPLE_SIZE,)) * note)
  oscillator2.process()
  mixer.set_input('in_data_1', oscillator2.get_output('out_data'))

  mixer.process()
  out_data = mixer.get_output('out_data')

  envelope.set_input('gate', gate)
  envelope.set_input('trigger', trigger)
  envelope.process()
  env = envelope.get_output('env')

  amplifier.set_input('vol_mod', env)
  amplifier.set_input('in_data', out_data)
  amplifier.process()
  out_data = amplifier.get_output('out_data')

  filter._param['freq_cut'] = 20 * 10 ** (2 * freq_cut)
  filter._param['res'] = res
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


lookup = {
        pygame.K_z: 12, # C
        pygame.K_s: 13, # C#
        pygame.K_x: 14, # D
        pygame.K_d: 15, # D#
        pygame.K_c: 16, # E
        pygame.K_v: 17, # F
        pygame.K_g: 18, # F#
        pygame.K_b: 19, # G
        pygame.K_h: 20, # G#
        pygame.K_n: 21, # A
        pygame.K_j: 22, # A#
        pygame.K_m: 23, # B
        pygame.K_COMMA: 24, # C
      }

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
      if clear:
        keys.clear()
        clear = False
      keys.append(event.key)
    elif event.type == pygame.KEYUP:
      if not sum(pygame.key.get_pressed()):
        gate = False
        clear = True
    elif event.type == pygame.MOUSEWHEEL:
      if pygame.key.get_pressed()[pygame.K_SPACE]:
        if event.y == 1:
          res = min(res + 0.05, 10.0)
        else:
          res = max(res - 0.05, 0.01)
      else:
        if event.y == 1:
          freq_cut = min(freq_cut + 0.05, 1.0)
        else:
          freq_cut = max(freq_cut - 0.05, 0.0)
      print(f'{freq_cut:.2f}    {res:.2f}')

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
