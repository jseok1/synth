import numpy as np
from modules.module import Module


class Envelope(Module):
  _offset: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._input = {
      'gate': np.zeros((sample_size + 1,)),
      'trigger': np.zeros((sample_size + 1,)),
      'att': np.ones((sample_size + 1,)),
      'att_mod': np.zeros((sample_size + 1,)),
      'att_mod_depth': np.zeros((sample_size + 1,)),
      'dec': np.ones((sample_size + 1,)),
      'dec_mod': np.zeros((sample_size + 1,)),
      'dec_mod_depth': np.zeros((sample_size + 1,)),
      'sus': np.ones((sample_size + 1,)),
      'sus_mod': np.zeros((sample_size + 1,)),
      'sus_mod_depth': np.zeros((sample_size + 1,)),
      'rel': np.ones((sample_size + 1,)),
      'rel_mod': np.zeros((sample_size + 1,)),
      'rel_mod_depth': np.zeros((sample_size + 1,)),
    }
    self._output = {
      'env': np.zeros((sample_size + 1,))  # range is [0, 1]
    }

    self._offset = np.inf

  def _ease(self, func, x, lower, upper):
    return func((x - lower) / (upper - lower)) * (upper - lower) + lower

  def _att(self, x: np.ndarray, att: np.ndarray) -> np.ndarray:
    mask = x < att

    y = np.zeros_like(x)
    y[mask] = self._ease(np.sqrt, x[mask] / att[mask], 0, 1)
    return y

  def _dec(
    self, x: np.ndarray, att: np.ndarray, dec: np.ndarray, sus: np.ndarray
  ) -> np.ndarray:
    mask = (att <= x) & (x < att + dec)

    y = np.zeros_like(x)
    y[mask] = self._ease(
      np.square,
      (sus[mask] - 1) / dec[mask] * (x[mask] - att[mask]) + 1,
      sus[mask],
      1,
    )
    return y

  def _sus(
    self, x: np.ndarray, att: np.ndarray, dec: np.ndarray, sus: np.ndarray
  ) -> np.ndarray:
    mask = att + dec <= x

    y = np.zeros_like(x)
    y[mask] = sus[mask]
    return y

  def _rel(self, x: np.ndarray, sus: np.ndarray, rel: np.ndarray) -> np.ndarray:
    mask = x < rel

    y = np.zeros_like(x)
    y[mask] = self._ease(
      np.square,
      -sus[mask] / rel[mask] * x[mask] + sus[mask],
      0,
      sus[mask],
    )
    return y

  def _att_offset(self, y: float, att: float) -> float:
    x = att * self._ease(np.square, y, 0, 1)
    return x

  def _rel_offset(self, y: float, sus: float, rel: float) -> float:
    x = -rel / sus * self._ease(np.sqrt, y, 0, sus) + rel
    return x

  def process(self):
    gate = self._input['gate']
    trigger = self._input['trigger']
    att = self._input['att']
    att_mod = self._input['att_mod']
    att_mod_depth = self._input['att_mod_depth']
    dec = self._input['dec']
    dec_mod = self._input['dec_mod']
    dec_mod_depth = self._input['dec_mod_depth']
    sus = self._input['sus']
    sus_mod = self._input['sus']
    sus_mod_depth = self._input['sus']
    rel = self._input['rel']
    rel_mod = self._input['rel_mod']
    rel_mod_depth = self._input['rel_mod_depth']

    env = self._output['env']
    env[:1], env[1:] = env[-1:], 0.0

    att *= 1 + att_mod * att_mod_depth
    dec *= 1 + dec_mod * dec_mod_depth
    sus *= 1 + sus_mod * sus_mod_depth
    rel *= 1 + rel_mod * rel_mod_depth

    diff = (gate[:-1] != gate[1:]) | (trigger[1:] > 0)
    (argdiff,) = np.where(np.concatenate([[False], diff, [True]]))

    low = 1
    for i, high in enumerate(argdiff):
      x = np.arange(high - low) / self._freq_sample

      if gate[low]:
        if i == 0:
          x += self._offset
        else:
          x += self._att_offset(env[low - 1], att[low])

        env[low:high] = (
          self._att(x, att[low:high])
          + self._dec(x, att[low:high], dec[low:high], sus[low:high])
          + self._sus(x, att[low:high], dec[low:high], sus[low:high])
        )
      else:
        if i == 0:
          x += self._offset
        else:
          x += self._rel_offset(env[low - 1], sus[low], rel[low])

        env[low:high] = self._rel(x, sus[low:high], rel[low:high])

      low = high

    self._offset = x[-1] + 1 / self._freq_sample

    gate[:1], gate[1:] = gate[-1:], 0.0
    trigger[:1], trigger[1:] = trigger[-1:], 0.0
    att[:1], att[1:] = att[-1:], 1.0
    att_mod[:1], att_mod[1:] = att_mod[-1:], 0.0
    att_mod_depth[:1], att_mod_depth[1:] = att_mod_depth[-1:], 0.0
    dec[:1], dec[1:] = dec[-1:], 1.0
    dec_mod[:1], dec_mod[1:] = dec_mod[-1:], 0.0
    dec_mod_depth[:1], dec_mod_depth[1:] = dec_mod_depth[-1:], 0.0
    rel[:1], rel[1:] = rel[-1:], 1.0
    rel_mod[:1], rel_mod[1:] = rel_mod[-1:], 0.0
    rel_mod_depth[:1], rel_mod_depth[1:] = rel_mod_depth[-1:], 0.0
    sus[:1], sus[1:] = sus[-1:], 1.0
    sus_mod[:1], sus_mod[1:] = sus_mod[-1:], 0.0
    sus_mod_depth[:1], sus_mod_depth[1:] = sus_mod_depth[-1:], 0.0
