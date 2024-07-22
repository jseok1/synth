import numpy as np

from modules.module import Module


class Mixer(Module):
  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._config = {
      'vol_1': 0.5,
      'vol_2': 0.5,
    }

    self._input = {
      'in_data_1': np.zeros((sample_size,)),
      'in_data_2': np.zeros((sample_size,)),
    }
    self._output = {'out_data': np.zeros((sample_size,))}

    self._data = np.zeros((sample_size + 2,))

  def process(self) -> None:
    vol_1 = self._config['vol_1']
    vol_2 = self._config['vol_2']

    in_data_1 = self._input['in_data_1']
    in_data_2 = self._input['in_data_2']

    out_data = self._output['out_data']
    out_data[:] = 0.0

    out_data[:] = vol_1 * in_data_1 + vol_2 * in_data_2

    in_data_1[:] = 0.0
    in_data_2[:] = 0.0
