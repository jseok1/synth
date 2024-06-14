import numpy as np

from modules.module import Module


# TODO: verify ADSR modulation is continuous, change trigger to same as osc

class Envelope(Module):
  _delta: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._param = {
      'att': 0.25,
      'att_mod_depth': 0.0,
      'dec': 0.35,
      'dec_mod_depth': 0.0,
      'sus': 0.5,
      'sus_mod_depth': 0.0,
      'rel': 0.5,
      'rel_mod_depth': 0.0,
    }

    self._input = {
      'att_mod': np.zeros((sample_size + 1,)),
      'dec_mod': np.zeros((sample_size + 1,)),
      'sus_mod': np.zeros((sample_size + 1,)),
      'rel_mod': np.zeros((sample_size + 1,)),
      'gate': np.zeros((sample_size + 1,)),
      'trigger': np.zeros((sample_size + 1,)),
    }
    self._output = {
      'env': np.zeros((sample_size + 1,))  # range is [0, 1]
    }

    self._delta = np.inf

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

  def _att_delta(self, y: float, att: float) -> float:
    x = att * self._ease(np.square, y, 0, 1)
    return x

  def _rel_delta(self, y: float, sus: float, rel: float) -> float:
    x = -rel / sus * self._ease(np.sqrt, y, 0, sus) + rel
    return x

  def process(self) -> None:
    att = self._param['att']
    att_mod_depth = self._param['att_mod_depth']
    dec = self._param['dec']
    dec_mod_depth = self._param['dec_mod_depth']
    sus = self._param['sus']
    sus_mod_depth = self._param['sus_mod_depth']
    rel = self._param['rel']
    rel_mod_depth = self._param['rel_mod_depth']

    att_mod = self._input['att_mod']
    dec_mod = self._input['dec_mod']
    sus_mod = self._input['sus_mod']
    rel_mod = self._input['rel_mod']
    gate = self._input['gate']
    trigger = self._input['trigger']

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
      if i == 0:
        delta = self._delta
      else:
        match gate[low]:
          case 0:
            delta = self._rel_delta(env[low - 1], sus[low], rel[low])
          case 1:
            delta = self._att_delta(env[low - 1], att[low])

      x = np.arange(high - low) / self._freq_sample + delta

      match gate[low]:
        case 0:
          env[low:high] = self._rel(x, sus[low:high], rel[low:high])
        case 1:
          env[low:high] = (
            self._att(x, att[low:high])
            + self._dec(x, att[low:high], dec[low:high], sus[low:high])
            + self._sus(x, att[low:high], dec[low:high], sus[low:high])
          )

      low = high

    self._delta = x[-1] + 1 / self._freq_sample

    att_mod[:1], att_mod[1:] = att_mod[-1:], 0.0
    dec_mod[:1], dec_mod[1:] = dec_mod[-1:], 0.0
    rel_mod[:1], rel_mod[1:] = rel_mod[-1:], 0.0
    sus_mod[:1], sus_mod[1:] = sus_mod[-1:], 0.0
    gate[:1], gate[1:] = gate[-1:], 0.0
    trigger[:1], trigger[1:] = trigger[-1:], 0.0
