import numpy as np


class Filter:
  def __init__(self, freq_sample, filters=2) -> None:
    self._freq_sample = freq_sample
    self._freq_cut_mod_depth = 1.0
    self._padding = np.zeros((filters + 1, 2))

    self.input = {
      # 'in_data':,
      # 'freq_cut':,
      # 'freq_cut_mod':,
      # 'freq_cut_mod_depth':,
      # 'res':,
      # 'res_mod':,
      # 'res_mod_depth':,
    }
    self.output = {}

  def _filter(self, sample_size, in_data, in_pad, out_pad, freq_cut, res):
    in_data = np.concatenate((in_pad, in_data))
    out_data = np.concatenate((out_pad, np.zeros(sample_size)))

    for i in range(sample_size):
      k = np.tan(np.pi * freq_cut[i] / self._freq_sample)
      q = 1 / np.sqrt(2) + res
      norm = 1 + k / q + k * k

      b = np.array([k * k / norm, 2 * k * k / norm, k * k / norm])
      a = np.array([1, 2 * (k * k - 1) / norm, (1 - k / q + k * k) / norm])

      out_data[i + 2] = np.dot(in_data[i : i + 3], b[::-1]) - np.dot(
        out_data[i : i + 2], a[:0:-1]
      )

    return out_data

  def process(self, sample_size, in_data, freq_cut, freq_cut_mod, res):
    # https://stackoverflow.com/questions/20924868/calculate-coefficients-of-2nd-order-butterworth-low-pass-filter
    # 12 or 24 dB/Oct slope? did I normalize right?
    # scale cutoff based on incoming pitch or just set freq?
    freq_cut *= 1 + self._freq_cut_mod_depth * freq_cut_mod

    # divide by sample rate????

    # TODO: normalize freq_cut_mod (and all other modulation params)

    in_pad = self._in_pad
    out_pad = self._out_pad[0, :]
    out_data = in_data
    for i in range(self.filters):
      out_data = self._filter(
        sample_size, out_data, in_pad, out_pad, freq_cut, res
      )
      in_pad = out_pad
      out_pad = self._out_pad[i, :]

    in_data = np.concatenate((self._in_pad, in_data))
    out_1_data_padded = np.concatenate(
      (self._out_1_pad, np.zeros(sample_size))
    )
    out_2_data = np.concatenate((self._out_2_pad, np.zeros(sample_size)))

    self._filter(sample_size, in_data, out_1_data, freq_cut, res)
    self._filter(sample_size, out_1_data, out_2_data, freq_cut, res)

    self._in_pad = in_data[-2:]
    self._out_1_pad = out_1_data[-2:]
    self._out_2_pad = out_2_data[-2:]

    return out_2_data[2:]


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
