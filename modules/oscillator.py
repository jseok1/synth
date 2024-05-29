import numpy as np
from module import Module


class Oscillator(Module):
  _offset: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._input = {
      'wave': np.zeros((sample_size,)),
      'freq': np.zeros((sample_size,)),
      'freq_mod': np.zeros((sample_size,)),
      'freq_mod_depth': np.zeros((sample_size,)),
    }
    self._output = {
      'out_data': np.zeros((sample_size,))  # range is [-1, 1]
    }

    self._offset = 0.0

  def _sin(self, x, wave):
    mask = wave == 0

    y = np.zeros_like(x)
    y[mask] = np.sin(2 * np.pi * x[mask])
    return y

  def _sqr(self, x, wave):
    mask = wave == 1

    y = np.zeros_like(x)
    y[mask] = np.sign(np.sin(2 * np.pi * x[mask]))
    return y

  def _tri(self, x, wave):
    mask = wave == 2

    y = np.zeros_like(x)
    y[mask] = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * x[mask]))
    return y

  def _saw(self, x, wave):
    mask = wave == 3

    y = np.zeros_like(x)
    y[mask] = 2 / np.pi * np.arctan(np.tan(np.pi * x[mask]))
    return y

  def process(self) -> None:
    wave = self._input['wave']
    freq = self._input['freq']
    freq_mod = self._input['freq_mod']
    freq_mod_depth = self._input['freq_mod_depth']

    out_data = self._output['out_data']
    out_data[:] = 0.0

    freq *= 1 + freq_mod_depth * freq_mod

    x = np.cumsum(freq) / self._freq_sample + self._offset

    out_data[:] = (
      self._sin(x, wave)
      + self._sqr(x, wave)
      + self._tri(x, wave)
      + self._saw(x, wave)
    )

    self._offset = x[-1] % 1

    wave[:] = 0.0
    freq[:] = 0.0
    freq_mod[:] = 0.0
    freq_mod_depth[:] = 0.0


if __name__ == '__main__':
  import matplotlib.pyplot as plt
  
  FREQ_SAMPLE = 44100
  SAMPLE_SIZE = 512

  out_data = []

  oscillator = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)

  oscillator.set_input('wave', np.ones((SAMPLE_SIZE,)) * 0)
  oscillator.set_input('freq', np.ones((SAMPLE_SIZE,)) * 400)
  oscillator.process()
  out_data.append(oscillator.get_output('out_data'))

  oscillator.set_input('wave', np.ones((SAMPLE_SIZE,)) * 0)
  oscillator.set_input('freq', np.ones((SAMPLE_SIZE,)) * 400)
  oscillator.process()
  out_data.append(oscillator.get_output('out_data'))

  oscillator.set_input('wave', np.ones((SAMPLE_SIZE,)) * 0)
  oscillator.set_input('freq', np.ones((SAMPLE_SIZE,)) * 400)
  oscillator.process()
  out_data.append(oscillator.get_output('out_data'))


  plt.figure()
  plt.plot(
    np.arange(SAMPLE_SIZE * 3) / FREQ_SAMPLE,
    np.concatenate(out_data),
  )
  plt.show()

  # https://stackoverflow.com/questions/26028763/how-to-change-parameters-realtimely-in-portaudio
