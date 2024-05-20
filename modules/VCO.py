import numpy as np


# it's a graph traversal technically using topological sort
# round robin for polyphonic synths with N voices

class VCO:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate
        self.phase_shift = 0
        self.freq_mod_percent = 0.0

    # range is [-1, 1]
    def process(self, t, sample_size, voltage, freq_mod, wave='saw'):
        freq = 8.175799 * 2 ** voltage / self.sample_rate # C-1 for reference
        freq *= np.ones((sample_size,)) + self.freq_mod_percent * freq_mod

        phase_shift = self.phase_shift + np.cumsum(freq)
        self.phase_shift = phase_shift[-1] % 1

        if wave == 'sine':
            out_data = np.sin(2 * np.pi * phase_shift)
        elif wave == 'square':
            out_data = np.sign(np.sin(2 * np.pi * phase_shift))
        elif wave == 'triangle':
            out_data = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * phase_shift))
        elif wave == 'saw':
            out_data = 2 / np.pi * np.arctan(np.tan(np.pi * phase_shift))

        return out_data
        # change pulse width by changing vertical shift of sign(sin)
    

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from LFO import LFO

    frame_count = 576
    vco = VCO(44100)
    lfo = LFO(44100)

    t = 576 * 9

    out_data1 = vco.process(t, frame_count, 5, lfo.process(t, frame_count))
    out_data2 = vco.process(t + 576, frame_count, 5, lfo.process(t + 576, frame_count))
    out_data2 = vco.process(t + 2 * 576, frame_count, 5, lfo.process(t + 2 * 576, frame_count))
    out_data2 = vco.process(t + 3 * 576, frame_count, 5, lfo.process(t + 3 * 576, frame_count))

    plt.figure()
    plt.plot(
        np.concatenate([(np.arange(frame_count) + t) / 44100, (np.arange(frame_count) + t + 576) / 44100]),
        np.concatenate([out_data1, out_data2]))
    plt.show() 

    # https://stackoverflow.com/questions/26028763/how-to-change-parameters-realtimely-in-portaudio