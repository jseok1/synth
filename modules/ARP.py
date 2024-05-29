import numpy as np


class ARP:

    def __init__(self, freq_sample) -> None:
        self._freq_sample = freq_sample
        self.notes = np.array([34, 38, 40, 41]) / 12
        # self.notes = np.array([36 / 12, 40 / 12, 43 / 12])
        self.t_offset = 0 # how far into the sequence
        self.order = 'asc'
        self.duration = 0.2
        self.glide_duration = 0.0

    def process(self, sample_size):
        
        # glide?

        pitch = np.zeros(sample_size)
        gate = np.zeros(sample_size)
        trigger = np.zeros(sample_size)
        velocity = np.zeros(sample_size)

        note = (np.arange(sample_size) + self.t_offset) // (self._freq_sample * self.duration) % self.notes.size
        note = note.astype(np.int32)
        pitch = self.notes[note]

        gate = np.ones(sample_size)

        # [0, 0, 0, 1, 1, 1]
        # [0, 0, 0, 1, 1, 1]
        # find where it changes, then interpolate 
        

        self.t_offset = (self.t_offset + sample_size) % (self._freq_sample * self.duration * self.notes.size)

        # TODO: elegant switching

        return pitch, gate, trigger, velocity
