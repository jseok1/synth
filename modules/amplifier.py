import numpy as np
from modules.module import Module


class Amplifier(Module):
  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._input = {
      'vol': np.ones((sample_size,)),
      'vol_mod': np.zeros((sample_size,)),
      'in_data': np.zeros((sample_size,)),
    }
    self._output = {'out_data': np.zeros((sample_size,))}

  def process(self) -> None:
    vol = self._input['vol']
    vol_mod = self._input['vol_mod']
    in_data = self._input['in_data']

    out_data = self._output['out_data']

    out_data[:] = 0.0

    vol *= vol_mod

    out_data[:] = in_data * vol

    vol[:] = 1.0
    vol_mod[:] = 0.0
    in_data[:] = 0.0
