import numpy as np


class Module:
  _freq_sample: float
  _sample_size: int
  _input: dict[str, np.ndarray]
  _output: dict[str, np.ndarray]

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    self._freq_sample = freq_sample
    self._sample_size = sample_size
    self._input = {}
    self._output = {}

  def set_input(self, input: str, data: np.ndarray):
    self._input[input][-self._sample_size :] = data

  def get_output(self, output: str):
    return self._output[output][-self._sample_size :][:]

  def process(self) -> None:
    raise NotImplementedError()
