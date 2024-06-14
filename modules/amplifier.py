import numpy as np

from modules.module import Module


# TODO: volume linear/log scale?

class Amplifier(Module):
  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._param = {'vol': 0.1}

    self._input = {
      'vol_mod': np.ones((sample_size,)),
      'in_data': np.zeros((sample_size,)),
    }
    self._output = {'out_data': np.zeros((sample_size,))}

  def process(self) -> None:
    vol = self._param['vol']

    vol_mod = self._input['vol_mod']
    in_data = self._input['in_data']

    out_data = self._output['out_data']
    out_data[:] = 0.0

    vol *= vol_mod

    # 20 * log10 
    # TODO: use RMS power

    out_data[:] = in_data * vol

    vol_mod[:] = 1.0
    in_data[:] = 0.0
