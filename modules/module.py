import numpy as np


class Module:
  _freq_sample: float
  _sample_size: int
  _params: dict[str, float]
  _input: dict[str, np.ndarray]
  _output: dict[str, np.ndarray]

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    self._freq_sample = freq_sample
    self._sample_size = sample_size
    self._params = {}
    self._in_channels = {}
    self._out_channels = {}

  def set_in_channel(self, in_channel: str, data: np.ndarray) -> None:
    self._in_channels[in_channel][-self._sample_size :] = np.copy(data)

  def get_out_channel(self, out_channel: str) -> np.ndarray:
    return np.copy(self._out_channels[out_channel][-self._sample_size :])

  def _shift_in_channels(self):
    for in_channel in self._in_channels:
      (
        self._in_channels[in_channel][: -self._sample_size],
        self._in_channels[in_channel][-self._sample_size :],
      ) = self._in_channels[in_channel][self._sample_size :], 0.0

  def _shift_out_channels(self):
    for out_channel in self._out_channels:
      (
        self._out_channels[out_channel][: -self._sample_size],
        self._out_channels[out_channel][-self._sample_size :],
      ) = self._out_channels[out_channel][self._sample_size :], 0.0

  def process(self) -> None:
    raise NotImplementedError()
