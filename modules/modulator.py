import numpy as np
from modules.module import Module


class Modulator(Module):
  _x_m1: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self.input = {
      'wave': 'TRI',
      'freq': np.zeros((sample_size,)),
      'freq_mod': np.zeros((sample_size,)),
      'freq_mod_depth': np.zeros((sample_size,)),
    }
    self.output = {
      'out_data': np.zeros((sample_size,))  # range is [0, 2] or [-1, 1]
    }
    
    self._x_m1 = 0.0

  def process(self) -> None:
    wave = self.input['wave']
    freq = self.input['freq']
    freq_mod = self.input['freq_mod']
    freq_mod_depth = self.input['freq_mod_depth']

    freq *= (1 + freq_mod_depth * freq_mod) / self._freq_sample
    x = (self._x_m1 + np.cumsum(freq)) % 1

    match wave:
      case 'SIN':
        out_data = np.sin(2 * np.pi * x) + 1
      case 'SQR':
        out_data = np.sign(np.sin(2 * np.pi * x)) + 1
      case 'TRI':
        out_data = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * x)) + 1
      case 'SAW':
        out_data = 2 / np.pi * np.arctan(np.tan(np.pi * x)) + 1
      case _:
        out_data = np.zeros((self._sample_size,))

    self.output['out_data'] = out_data

    self._x_m1 = x[-1]
