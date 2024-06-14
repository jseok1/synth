import numpy as np

from modules.module import Module


class Oscillator(Module):
  _delta: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._param = {
      'wave': 4,
      'freq': 8.175799 * 2**2,
      'freq_mod_depth': 0.0,
      'pulse_width': 0.8,
      'pulse_width_mod_depth': 0.0,
    }

    self._input = {
      'freq_mod': np.zeros((sample_size + 1,)),
      'pulse_width_mod': np.zeros((sample_size + 1,)),
      'note': np.zeros((sample_size + 1,)),
      'sync': -np.ones((sample_size + 1,)),
    }
    self._output = {
      'out_data': np.zeros((sample_size + 1,))  # range is [-1, 1]
    }

    self._delta = 0.0

  def _sine(self, x):
    y = np.sin(2 * np.pi * x)
    return y

  def _triangle(self, x):
    y = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * x))
    return y

  def _sawtooth(self, x):
    y = 2 / np.pi * np.arctan(np.tan(np.pi * x))
    return y

  def _square(self, x):
    y = np.sign(np.sin(2 * np.pi * x))
    return y

  def _pulse(self, x, pulse_width):
    y = np.sign(
      np.arcsin(np.sin(2 * np.pi * (x - pulse_width / 2 + 1 / 4)))
      + np.pi * pulse_width
      - np.pi / 2
    )
    return y

  def process(self) -> None:
    wave = self._param['wave']
    freq = self._param['freq']
    freq_mod_depth = self._param['freq_mod_depth']
    pulse_width = self._param['pulse_width']
    pulse_width_mod_depth = self._param['pulse_width_mod_depth']

    freq_mod = self._input['freq_mod']
    pulse_width_mod = self._input['pulse_width_mod']
    note = self._input['note']
    sync = self._input['sync']

    out_data = self._output['out_data']
    out_data[:1], out_data[1:] = out_data[-1:], 0.0

    freq *= 2 ** (note / 12) * (1 + freq_mod_depth * freq_mod)
    pulse_width *= 1 + pulse_width_mod_depth * pulse_width_mod

    pulse_width = np.clip(pulse_width, 0.01, 0.99)

    delta = self._delta

    x = np.zeros((self._sample_size + 1,))

    # first time it's >= 0 or > 0?
    diff = np.diff(np.clip(np.sign(sync), -1, 0)) == 1
    (argdiff,) = np.where(np.concatenate([[False], diff, [True]]))

    low = 1
    for i, high in enumerate(argdiff):
      if i == 0:
        delta = self._delta
      else:
        delta = 0
      x[low:high] = np.cumsum(freq[low:high] / self._freq_sample) + delta

    match wave:
      case 0:
        out_data[1:] = self._sine(x[1:])
      case 1:
        out_data[1:] = self._triangle(x[1:])
      case 2:
        out_data[1:] = self._sawtooth(x[1:])
      case 3:
        out_data[1:] = self._square(x[1:])
      case 4:
        out_data[1:] = self._pulse(x[1:], pulse_width[1:])

    self._delta = x[-1] % 1

    freq_mod[:1], freq_mod[1:] = freq_mod[-1:], 0.0
    note[:1], note[1:] = note[-1:], 0
    sync[:1], sync[1:] = sync[-1:], 0.0


if __name__ == '__main__':
  import matplotlib.pyplot as plt

  FREQ_SAMPLE = 44100
  SAMPLE_SIZE = 512

  out_data = []
  sync = []

  leader = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)
  follower = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)

  leader._param['wave'] = 3
  follower._param['wave'] = 2

  n = 50
  for i in range(n):
    note = np.ones((SAMPLE_SIZE,))

    leader.set_input('note', note)
    leader.process()
    sync.append(leader.get_output('out_data'))

    follower.set_input('note', note * 0.9)
    follower.set_input('sync', sync[-1])
    follower.process()
    out_data.append(follower.get_output('out_data'))

  plt.figure()
  plt.plot(
    np.arange(SAMPLE_SIZE * n) / FREQ_SAMPLE,
    np.concatenate(sync),
  )
  plt.plot(
    np.arange(SAMPLE_SIZE * n) / FREQ_SAMPLE,
    np.concatenate(out_data),
  )
  plt.show()

  # https://stackoverflow.com/questions/26028763/how-to-change-parameters-realtimely-in-portaudio
