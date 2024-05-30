import numpy as np

from modules.module import Module


class Oscillator(Module):
  _delta: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._param = {
      'wave': 3,
      'freq': 8.175799 * 2**2,
      'freq_mod_depth': 0.0,
    }

    self._input = {
      'freq_mod': np.zeros((sample_size,)),
      'note': np.zeros((sample_size,)),
    }
    self._output = {
      'out_data': np.zeros((sample_size,))  # range is [-1, 1]
    }

    self._delta = 0.0

  def _sin(self, x):
    y = np.sin(2 * np.pi * x)
    return y

  def _sqr(self, x):
    y = np.sign(np.sin(2 * np.pi * x))
    return y

  def _tri(self, x):
    y = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * x))
    return y

  def _saw(self, x):
    y = 2 / np.pi * np.arctan(np.tan(np.pi * x))
    return y

  def process(self) -> None:
    wave = self._param['wave']
    freq = self._param['freq']
    freq_mod_depth = self._param['freq_mod_depth']

    freq_mod = self._input['freq_mod']
    note = self._input['note']

    out_data = self._output['out_data']
    out_data[:] = 0.0

    freq *= 2 ** (note / 12) * (1 + freq_mod_depth * freq_mod)

    x = np.cumsum(freq / self._freq_sample) + self._delta

    match wave:
      case 0:
        out_data[:] = self._sin(x)
      case 1:
        out_data[:] = self._sqr(x)
      case 2:
        out_data[:] = self._tri(x)
      case 3:
        out_data[:] = self._saw(x)

    self._delta = x[-1] % 1

    freq_mod[:] = 0.0
    note[:] = 0


if __name__ == '__main__':
  import matplotlib.pyplot as plt

  FREQ_SAMPLE = 44100
  SAMPLE_SIZE = 512

  out_data = []

  oscillator = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)

  n = 100
  for _ in range(n):
    oscillator.set_input('note', np.ones((SAMPLE_SIZE,)) * 10)
    oscillator.process()
    out_data.append(oscillator.get_output('out_data'))

  plt.figure()
  plt.plot(
    np.arange(SAMPLE_SIZE * n) / FREQ_SAMPLE,
    np.concatenate(out_data),
  )
  plt.show()

  # https://stackoverflow.com/questions/26028763/how-to-change-parameters-realtimely-in-portaudio
