import numpy as np


class LFO:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate
        self.depth = 0.1
        self.area = 0

    def process(self, t, sample_size):
        t = (np.arange(sample_size) + t) / self.sample_rate
        
        frequency = 1
        out_data = self.depth * np.sin(2 * np.pi * frequency * t) # but what does a negative frequency mean?
        out_data_integral = self.area + np.cumsum(out_data)
        self.area = out_data_integral[-1]

        return out_data_integral.astype(np.float32)
    