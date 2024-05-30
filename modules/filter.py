import numpy as np

from modules.module import Module


class Filter(Module):
  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._param = {
      'freq_cut': 2000.0,
      'freq_cut_mod_depth': 0.5,
      'res': 0.0,
      'res_mod_depth': 0.0,
    }

    self._input = {
      'freq_cut_mod': np.zeros((sample_size + 2,)),
      'res_mod': np.zeros((sample_size + 2,)),
      'in_data': np.zeros((sample_size + 2,)),
    }
    self._output = {'out_data': np.zeros((sample_size + 2,))}

    self._data = np.zeros((sample_size + 2,))

  def _filter(self, in_data, out_data, freq_cut, res):
    for i in range(2, self._sample_size + 2):
      k = np.tan(np.pi * freq_cut[i] / self._freq_sample)
      q = 1 / np.sqrt(2) + res[i]
      norm = 1 + k / q + k * k

      b = np.array([k * k, 2 * k * k, k * k]) / norm
      a = np.array([2 * (k * k - 1), (1 - k / q + k * k)]) / norm

      out_data[i] = np.dot(in_data[i - 2 : i + 1], b[::-1]) - np.dot(
        out_data[i - 2 : i], a[::-1]
      )

  def process(self) -> None:
    freq_cut = self._param['freq_cut']
    freq_cut_mod_depth = self._param['freq_cut_mod_depth']
    res = self._param['res']
    res_mod_depth = self._param['res_mod_depth']

    freq_cut_mod = self._input['freq_cut_mod']
    res_mod = self._input['res_mod']
    in_data = self._input['in_data']

    out_data = self._output['out_data']
    out_data[:2], out_data[2:] = out_data[-2:], 0.0

    self._data[:2], self._data[2:] = self._data[-2:], 0.0

    freq_cut *= 1 + freq_cut_mod_depth * freq_cut_mod
    res *= np.ones(self._sample_size + 2) # TODO

    self._filter(in_data, self._data, freq_cut, res)
    self._filter(self._data, out_data, freq_cut, res)

    freq_cut_mod[:2], freq_cut_mod[2:] = freq_cut_mod[-2:], 0.0
    res_mod[:2], res_mod[2:] = res_mod[-2:], 0.0
    in_data[:2], in_data[2:] = in_data[-2:], 0.0

    # https://stackoverflow.com/questions/20924868/calculate-coefficients-of-2nd-order-butterworth-low-pass-filter
    # 12 or 24 dB/Oct slope? did I normalize right?
    # scale cutoff based on incoming pitch or just set freq?
    # divide by sample rate????


if __name__ == '__main__':
  import numpy as np
  import matplotlib.pyplot as plt

  from modules.Oscillator import Oscillator

  Oscillator = Oscillator(44100)
  Filter = Filter(44100)

  t = 0
  data1 = Oscillator.process(t, 576, 5, 1, 'saw')
  data2 = Filter.process(576, data1, 20 * 10 ** (3 * 0.3), 0.0)
  data3 = Filter.process(576, data1, 20 * 10 ** (3 * 0.3), 2.0)

  plt.figure()
  plt.plot(np.arange(576) / 44100, data1)
  plt.plot(np.arange(576) / 44100, data2)
  plt.plot(np.arange(576) / 44100, data3)
  plt.show()

  # TODO: ensure stability
  # plot
