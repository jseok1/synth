import numpy as np

from modules.module import Module


# TODO: glide, pause


class Arpeggiator(Module):
  def __init__(self, freq_sample: float, sample_size: int) -> None:
    super().__init__(freq_sample, sample_size)

    self._param = {
      'notes': np.array([]),
      'direction': 0,
      'duration': 0.25,
      'glide': 0.0,
      'octaves': 2,
    }

    self._input = {}
    self._output = {
      'note': np.zeros((sample_size + 1,)),
      'gate': np.zeros((sample_size + 1,)),
      'trigger': np.zeros((sample_size + 1,)),
    }

    self._delta = 0.0

  def process(self):
    notes = self._param['notes']
    direction = self._param['direction']
    duration = self._param['duration']
    glide = self._param['glide']
    octaves = self._param['octaves']

    note = self._output['note']
    gate = self._output['gate']
    trigger = self._output['trigger']
    note[:1], note[1:] = note[-1:], 0.0
    gate[:1], gate[1:] = gate[-1:], 0.0
    trigger[:1], trigger[1:] = trigger[-1:], 0.0

    if direction == 0:
      notes = np.sort(notes)

    n = notes.size
    for i in range(1, octaves):
      notes = np.concatenate([notes, np.copy(notes[-n:]) + 12 * i])

    x = np.arange(self._sample_size) + self._delta

    # actually don't think we need notes.size
    note[1:] = notes[(x // (self._freq_sample * duration) % notes.size).astype(int)]
    gate[1:] = 1.0
    trigger[1:] = note[:-1] != note[1:]



    # [0, 0, 0, 1, 1, 1]
    # [0, 0, 0, 1, 1, 1]
    # find where it changes, then interpolate

    self._delta = x[-1] % (self._freq_sample * duration * notes.size)

    # TODO: elegant switching