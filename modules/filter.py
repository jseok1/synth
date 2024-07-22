import numpy as np

from module import Module

# TODO: key tracking, -3dB cutoff?, resonance range and scale?, cascading filter correction


class Filter(Module):
  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._params = {
      'freq_cut': 2000.0,
      'freq_cut_mod_amt': 0.5,
      'res': 1 / np.sqrt(2),
      'res_mod_amt': 0.0,
    }
    self._in_channels = {
      'in_freq_cut_mod': np.zeros((sample_size + 2,)),
      'in_res_mod': np.zeros((sample_size + 2,)),
      'in_data': np.zeros((sample_size + 2,)),
    }
    self._out_channels = {
      'out_data': np.zeros((sample_size + 2,)),
    }

    self._buffer = np.zeros((sample_size + 2,))

  def _filter(
    self,
    in_data: np.ndarray,
    out_data: np.ndarray,
    freq_cut: np.ndarray,
    res: np.ndarray,
  ):
    # w in rad/sec
    # w = 2pi f
    #
    # w_c = 2 / T tan(w_d T / 2)
    # w_c = 2 * freq_sample * tan(pi freq / sample_freq) <- angular freq cut
    #
    # -3dB is 1/2 drop in power
    # power \prop |H(jw_c)|^2 = 1 / 2
    # |H(jw_c)| = 1 / sqrt(1 + (w/w_cut)^2) = 1 / sqrt(2)
    # solving..
    # w = w_cut sqrt(sqrt(2) - 1)
    # impulse response function
    # difference is due to the nonlinearity of the bilinear transform

    # H_d(z) = H_a(2 / T (z - 1) / (z + 1))
    # z = e^(j w_d T)
    # H_d(e^(j w_d T)) = H_a(j w_c)
    #                  = H_a(j 2 / T tan(w_d T / 2))

    # w_c = w_c_cut sqrt(sqrt(2) - 1)
    # w_c_cut = w_c / sqrt(sqrt(2) - 1))

    freq_cut = np.tan(np.pi * freq_cut / self._freq_sample)
    # freq_cut = np.tan(np.pi * freq_cut / self._freq_sample / np.sqrt(np.sqrt(2) - 1))
    # otherwise at most pi / 2 bc of Nyquist
    # ~ 1.574642359592092 --> greater than pi / 2 (domain error)
    # -260.0069011549437

    freq_cut_sqr = freq_cut * freq_cut
    norm = 1 + freq_cut / res + freq_cut_sqr

    b = np.array(
      [
        freq_cut_sqr,
        2 * freq_cut_sqr,
        freq_cut_sqr,
      ]
    )
    a = np.array(
      [
        2 * freq_cut_sqr - 2,
        1 - freq_cut / res + freq_cut_sqr,
      ]
    )
    b = (b / norm).T
    a = (a / norm).T

    for i in range(2, self._sample_size + 2):
      out_data[i] = np.dot(in_data[i - 2 : i + 1], b[i, ::-1]) - np.dot(
        out_data[i - 2 : i], a[i, ::-1]
      )

  def process(self) -> None:
    freq_cut = self._params['freq_cut']
    freq_cut_mod_amt = self._params['freq_cut_mod_amt']
    res = self._params['res']
    res_mod_amt = self._params['res_mod_amt']

    in_freq_cut_mod = self._in_channels['in_freq_cut_mod']
    in_res_mod = self._in_channels['in_res_mod']
    in_data = self._in_channels['in_data']

    out_data = self._out_channels['out_data']

    self._shift_out_channels()
    self._buffer[:2], self._buffer[2:] = self._buffer[-2:], 0.0

    freq_cut *= 1 + freq_cut_mod_amt * in_freq_cut_mod
    res *= 1 + res_mod_amt * in_res_mod

    self._filter(in_data, self._buffer, freq_cut, 1 / (2 * np.cos(np.pi / 8)) + 10)
    self._filter(self._buffer, out_data, freq_cut, 1 / (2 * np.cos(3 * np.pi / 8)) + 10)

    self._shift_in_channels()


if __name__ == '__main__':
  import numpy as np
  import matplotlib.pyplot as plt

  from scipy.ndimage import gaussian_filter1d
  from oscillator import Oscillator

  from scipy.signal import butter, lfilter

  FREQ_SAMPLE = 44100
  SAMPLE_SIZE = 512

  plt.figure()
  colors = ['tab:blue', 'tab:orange', 'tab:green']

  for i, freq_cut in enumerate([5000, 10000, 15000]):  # 14226 to 14227
    out_data1 = []  # not filtered
    out_data2 = []  # filtered

    oscillator = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)
    filter = Filter(FREQ_SAMPLE, SAMPLE_SIZE)

    filter._params['freq_cut'] = freq_cut
    filter._params['res'] = 1 / np.sqrt(2)

    n = 250
    for _ in range(n):
      oscillator.set_in_channel('in_volt_per_oct', np.ones((SAMPLE_SIZE,)) * 9)
      oscillator.process()
      out_data1.append(oscillator.get_out_channel('out_pul'))

      filter.set_in_channel('in_data', out_data1[-1])
      filter.process()
      out_data2.append(filter.get_out_channel('out_data'))

    out_data1 = np.concatenate(out_data1)
    out_data2 = np.concatenate(out_data2)

    b, a = butter(4, freq_cut, fs=FREQ_SAMPLE)
    out_data3 = lfilter(b, a, out_data1)
    # out_data3 = lfilter(b, a, out_data3)

    





    fft1 = np.abs(np.fft.fft(out_data1)) / (n * SAMPLE_SIZE)
    fft2 = np.abs(np.fft.fft(out_data2)) / (n * SAMPLE_SIZE)
    fft3 = np.abs(np.fft.fft(out_data3)) / (n * SAMPLE_SIZE)

    freqs = np.fft.fftfreq(n * SAMPLE_SIZE, 1 / FREQ_SAMPLE)

    gain2 = gaussian_filter1d(20 * np.log10(fft2 / fft1), 500)
    gain3 = gaussian_filter1d(20 * np.log10(fft3 / fft1), 500)

    plt.plot(
      freqs[: n * SAMPLE_SIZE // 2],
      gain2[: n * SAMPLE_SIZE // 2],
      color=colors[i],
    )
    plt.plot(
      freqs[: n * SAMPLE_SIZE // 2],
      gain3[: n * SAMPLE_SIZE // 2],
      color=colors[i],
      alpha=0.5,
    )
    plt.axvline(freq_cut, ls='--', color='grey')

  plt.axhline(-3, ls='--', color='red')
  # plt.axhline(-6, ls='--', color='red')
  plt.show()
