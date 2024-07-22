import numpy as np

from module import Module


class Oscillator(Module):
  _delta: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._params = {
      'freq': 8.175799 * 2**2,  # 32': 2, 16': 3, 8': 4, 4': 5, 2': 6
      'freq_mod_amt': 0.0,
      'pul_width': 0.5,
      'pul_width_mod_amt': 0.0,
    }
    self._in_channels = {
      'in_freq_mod': np.zeros((sample_size + 1,)),
      'in_pul_width_mod': np.zeros((sample_size + 1,)),
      'in_volt_per_oct': np.zeros((sample_size + 1,)),
      'in_sync': np.zeros((sample_size + 1,)),
    }
    self._out_channels = {
      'out_sin': np.zeros((sample_size + 1,)),  # range is [-1, 1]
      'out_tri': np.zeros((sample_size + 1,)),
      'out_saw': np.zeros((sample_size + 1,)),
      'out_pul': np.zeros((sample_size + 1,)),
    }

    self._delta = 0.0

  def _sin(self, x):
    y = np.sin(2 * np.pi * x)
    return y

  def _tri(self, x):
    y = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * x))
    return y

  def _saw(self, x):
    y = 2 / np.pi * np.arctan(np.tan(np.pi * x))
    return y

  def _pul(self, x, pul_width):
    y = np.sign(
      np.arcsin(np.sin(2 * np.pi * x - np.pi * pul_width + np.pi / 2))
      + np.pi * pul_width
      - np.pi / 2
    )
    return y

  def process(self) -> None:
    freq = self._params['freq']
    freq_mod_amt = self._params['freq_mod_amt']
    pul_width = self._params['pul_width']
    pul_width_mod_amt = self._params['pul_width_mod_amt']

    in_freq_mod = self._in_channels['in_freq_mod']
    in_pul_width_mod = self._in_channels['in_pul_width_mod']
    in_volt_per_oct = self._in_channels['in_volt_per_oct']
    in_sync = self._in_channels['in_sync']

    out_sin = self._out_channels['out_sin']
    out_tri = self._out_channels['out_tri']
    out_saw = self._out_channels['out_saw']
    out_pul = self._out_channels['out_pul']

    self._shift_out_channels()

    freq *= 2**in_volt_per_oct * (1 + in_freq_mod * freq_mod_amt)
    pul_width *= 1 + in_pul_width_mod * pul_width_mod_amt
    pul_width = np.clip(pul_width, 0.01, 0.99)

    diff = (in_sync[:-1] < 0) & (in_sync[1:] >= 0)
    (argdiff,) = np.where(np.concatenate([diff, [True]]))
    argdiff += 1

    x = np.zeros((self._sample_size + 1,))
    low = 1
    for i, high in enumerate(argdiff):
      x[low:high] = np.cumsum(freq[low:high]) / self._freq_sample
      if i == 0:
        x[low:high] += self._delta
      low = high

    out_sin[1:] = self._sin(x[1:])
    out_tri[1:] = self._tri(x[1:])
    out_saw[1:] = self._saw(x[1:])
    out_pul[1:] = self._pul(x[1:], pul_width[1:])

    # low = 1
    # for i, high in enumerate(argdiff):
    #   x = np.cumsum(freq[low:high]) / self._freq_sample
    #   if i == 0:
    #     x += self._delta
    #   out_sin[low:high] = self._sin(x)
    #   out_tri[low:high] = self._tri(x)
    #   out_saw[low:high] = self._saw(x)
    #   out_pul[low:high] = self._pul(x, pul_width[low:high])
    #   low = high

    self._shift_in_channels()
    self._delta = x[-1] % 1
