import numpy as np

from modules.module import AbstractModule


class ModulatorModule(AbstractModule):
  _delta: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._params = {
      'freq': 8.175799 * 2**3,  # 32': 2, 16': 3, 8': 4, 4': 5, 2': 6
      'freq_mod_amt': 0.0,
      'pul_width': 0.5,
      'pul_width_mod_amt': 0.0,
    }
    self._in_channels = {
      'in_freq_mod': np.zeros((sample_size + 1,)),
      'in_pul_width_mod': np.zeros((sample_size + 1,)),
      'in_reset': np.zeros((sample_size + 1,)),
    }
    self._out_channels = {
      'out_sin': np.zeros((sample_size + 1,)),  # range is [-1, 1]
      'out_tri': np.zeros((sample_size + 1,)),
      'out_saw': np.zeros((sample_size + 1,)),
      'out_pul': np.zeros((sample_size + 1,)),
    }

    self._delta = 0.0

  def process(self) -> None:
    freq = self._params['freq']
    freq_mod_amt = self._params['freq_mod_amt']
    pul_width = self._params['pul_width']
    pul_width_mod_amt = self._params['pul_width_mod_amt']

    in_freq_mod = self._in_channels['in_freq_mod']
    in_pul_width_mod = self._in_channels['in_pul_width_mod']
    in_volt_per_oct = self._in_channels['in_volt_per_oct']
    in_reset = self._in_channels['in_reset']

    out_sin = self._out_channels['out_sin']
    out_tri = self._out_channels['out_tri']
    out_saw = self._out_channels['out_saw']
    out_pul = self._out_channels['out_pul']

    self._shift_out_channels()

    freq *= 2**in_volt_per_oct * (1 + in_freq_mod * freq_mod_amt)
    pul_width *= 1 + in_pul_width_mod * pul_width_mod_amt
    pul_width = np.clip(pul_width, 0.01, 0.99)

    phase = np.zeros((self._sample_size + 1,))

    diff = (in_reset[:-1] < 0) & (in_reset[1:] >= 0)
    (argdiff,) = np.where(np.concatenate([diff, [True]]))
    argdiff += 1

    low = 1
    for i, high in enumerate(argdiff):
      if i == 0:
        phase[low:high] += self._delta
      phase[low:high] += np.cumsum(freq[low:high]) / self._freq_sample
      phase[low:high] %= 1
      low = high

    self._delta = phase[-1]

    out_sin[1:] = np.sin(2 * np.pi * phase[1:])
    out_tri[1:] = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * phase[1:]))
    out_saw[1:] = 2 / np.pi * np.arctan(np.tan(np.pi * phase[1:]))
    out_pul[1:] = np.sign(
      np.arcsin(
        np.sin(2 * np.pi * phase[1:] - np.pi * pul_width[1:] + np.pi / 2)
      )
      + np.pi * pul_width[1:]
      - np.pi / 2
    )

    self._shift_in_channels()
