import numpy as np


class LFO:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate

    # range is [0, 2]
    def process(self, t, sample_size, wave='sine'):
        t = (np.arange(sample_size) + t) / self.sample_rate
        
        # LFO goes [0, 10]
        freq = 2

        # TODO: also add freq modulation, clock modulation

        if wave == 'sine':
            out_data = np.sin(2 * np.pi * freq * t) + 1
        elif wave == 'square':
            out_data = np.sign(np.sin(2 * np.pi * freq * t)) + 1
        elif wave == 'triangle':
            out_data = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * freq * t)) + 1
        elif wave == 'saw':
            out_data = 2 / np.pi * np.arctan(np.tan(np.pi * freq * t)) + 1
        
        return out_data
    