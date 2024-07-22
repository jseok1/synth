import numpy as np

from modules.module import AbstractModule


# TODO: verify ADSR modulation is continuous, change trig to same as osc


class EnvelopeModule(AbstractModule):
  _delta: float

  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._params = {
      'att': 0.25,
      'att_mod_amt': 0.0,
      'dec': 0.35,
      'dec_mod_amt': 0.0,
      'sus': 0.5,
      'sus_mod_amt': 0.0,
      'rel': 0.5,
      'rel_mod_amt': 0.0,
    }
    self._in_channels = {
      'in_att_mod': np.zeros((sample_size + 1,)),
      'in_dec_mod': np.zeros((sample_size + 1,)),
      'in_sus_mod': np.zeros((sample_size + 1,)),
      'in_rel_mod': np.zeros((sample_size + 1,)),
      'in_gate': np.zeros((sample_size + 1,)),
      'in_trig': np.zeros((sample_size + 1,)),
    }
    self._out_channels = {
      'out_env': np.zeros((sample_size + 1,)),  # range is [0, 1]
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
      np.square, -sus[mask] / rel[mask] * x[mask] + sus[mask], 0, sus[mask]
    )
    return y

  def _att_delta(self, y: float, att: float) -> float:
    x = att * self._ease(np.square, y, 0, 1)
    return x

  def _rel_delta(self, y: float, sus: float, rel: float) -> float:
    x = -rel / sus * self._ease(np.sqrt, y, 0, sus) + rel
    return x

  def _env(self, gate, att, dec, sus, rel) -> np.ndarray:
    if gate:
      # TODO: potential optimization
      out_env[low:high] = (
        self._att(x[low:high], att[low:high])
        + self._dec(x[low:high], att[low:high], dec[low:high], sus[low:high])
        + self._sus(x[low:high], att[low:high], dec[low:high], sus[low:high])
      )
    else:
      out_env[low:high] = self._rel(x[low:high], sus[low:high], rel[low:high])

  def process(self) -> None:
    att = self._params['att']
    att_mod_amt = self._params['att_mod_amt']
    dec = self._params['dec']
    dec_mod_amt = self._params['dec_mod_amt']
    sus = self._params['sus']
    sus_mod_amt = self._params['sus_mod_amt']
    rel = self._params['rel']
    rel_mod_amt = self._params['rel_mod_amt']

    in_att_mod = self._in_channels['in_att_mod']
    in_dec_mod = self._in_channels['in_dec_mod']
    in_sus_mod = self._in_channels['in_sus_mod']
    in_rel_mod = self._in_channels['in_rel_mod']
    in_gate = self._in_channels['in_gate']
    in_trig = self._in_channels['in_trig']

    out_env = self._out_channels['out_env']

    self._shift_out_channels()

    att *= 1 + in_att_mod * att_mod_amt
    dec *= 1 + in_dec_mod * dec_mod_amt
    sus *= 1 + in_sus_mod * sus_mod_amt
    rel *= 1 + in_rel_mod * rel_mod_amt

    diff = (in_gate[:-1] != in_gate[1:]) | (in_trig[:-1] < 0) & (in_trig[1:] >= 0)
    (argdiff,) = np.where(np.concatenate([diff, [True]]))
    argdiff += 1

    x = np.zeros((self._sample_size + 1,))
    low = 1
    for i, high in enumerate(argdiff):
      x[low:high] = np.arange(high - low) / self._freq_sample
      if i == 0:
        x[low:high] += self._delta
      else:
        if in_gate[low]:
          x[low:high] += self._att_delta(out_env[low - 1], att[low])
        else:
          x[low:high] += self._rel_delta(out_env[low - 1], sus[low], rel[low])
      out_env[low:high] = self._env(in_gate[low], att[low:high], dec[low:high], sus[low:high], rel[low:high])
      low = high

    self._shift_in_channels()
    self._delta = x[-1] + 1 / self._freq_sample
