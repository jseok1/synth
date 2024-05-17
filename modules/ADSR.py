import numpy as np


class ADSR:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate
   
        self.t_offset = 0
        self.gate = 0

    # def interpolate(x, lower, upper, func):
    #     return func((x - lower) / (upper - lower)) * (upper - lower) + lower

    def attack(self, t, attack):
        out_data = np.cbrt(t / attack)
        return out_data
    
    def decay(self, t, attack, decay, sustain):
        out_data = np.power(((sustain - 1) / decay * (t - attack) + 1 - sustain) / (1 - sustain), 3) * (1 - sustain) + sustain
        return out_data
    
    def sustain(self, sustain):
        out_data = sustain
        return out_data
    
    def release(self, t, sustain, release):
        return np.power(1 - t / release, 3) * sustain

    # # https://dsp.stackexchange.com/questions/2555/help-with-equations-for-exponential-adsr-envelope
    def process(self, t, sample_size, gate, attack, decay, sustain, release):
        gate = gate > 0

        out_data = np.zeros((sample_size,))

        t = np.zeros((sample_size,))

        groups = np.concatenate(([0], (gate[:-1] != gate[1:]).cumsum()))
        for group in np.unique(groups):
            mask = groups == group
            t[mask] = np.arange(np.sum(mask)) / self.sample_rate
            if group == 0 and self.gate == gate[0]:
                t[mask] += self.t_offset
        
        self.t_offset = t[-1] + 1 / self.sample_rate
        self.gate = gate[-1]

        mask = gate & (t < attack)
        out_data[mask] = self.attack(t[mask], attack[mask])

        mask = gate & (attack <= t) & (t < attack + decay)
        out_data[mask] = self.decay(t[mask], attack[mask], decay[mask], sustain[mask])

        mask = gate & (attack + decay <= t)
        out_data[mask] = self.sustain(sustain[mask])

        mask = ~gate & (t < release)
        out_data[mask] = self.release(t[mask], sustain[mask], release[mask])

        return out_data.astype(np.float32)
    

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    adsr = ADSR(44100)
    out_data1 = adsr.process(0, 576,
                       0.003 + (0.001 * np.sin(2 * np.pi * (1 / 0.003) * np.arange((576))) + 0.001),
                       np.ones((576)) * 0.003,
                       np.ones((576)) * 0.003,
                       np.ones((576)) * 0.5,
                       np.ones((576)) * 0.005
                       )

    out_data2 = adsr.process(576, 576,
                       np.ones((576)),
                       np.ones((576)) * 0.003,
                       np.ones((576)) * 0.003,
                       np.ones((576)) * 0.5,
                       np.ones((576)) * 0.005
                       )
    
    out_data3 = adsr.process(576 + 576, 576,
                       np.zeros((576)),
                       np.ones((576)) * 0.003,
                       np.ones((576)) * 0.003,
                       np.ones((576)) * 0.5,
                       np.ones((576)) * 0.005
                       )
    
    plt.figure()
    plt.plot((np.arange(576 * 3)) / 44100, np.concatenate((out_data1, out_data2, out_data3)))
    plt.show()

