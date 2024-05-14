import numpy as np


class ADSR:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate
        self.attack = 0 # x_a (attack time)
        self.decay = 0 # x_d (decay time)
        self.sustain = 0 # y_s (sustain level)
        self.release = 0 # x_r (release time)

        self.t_press = 0
        self.t_release = 0

    # def interpolate(x, lower, upper, func):
    #     return func((x - lower) / (upper - lower)) * (upper - lower) + lower

    def attack(self, x, attack):
        mask = x < attack
        out_data = np.zeros_like(x)
        out_data[mask] = np.cbrt(x[mask] / attack[mask])
        return out_data
    
    def decay(self, x, attack, decay, sustain):
        mask = attack <= x < decay
        out_data = np.zeros_like(x)
        out_data[mask] = np.power(((sustain[mask] - 1) / decay[mask] * (x[mask] - attack[mask]) + 1 - sustain[mask]) / (1 - sustain[mask]), 3) * (1 - sustain[mask]) + sustain[mask]
        return out_data
    
    def sustain(self, x, decay, sustain):
        mask = decay <= x 
        out_data = np.zeros_like(x)
        out_data[mask] = sustain[mask]
        return out_data
    
    # def release(self, x, attack, decay, sustain, release):
    #     # needs to be squished though
    #     x[~(release <= x < release)] = 0
    #     return np.power((attack + decay + ? - x) / release + 1, 3) * sustain


    # np.piecewise(x, [x < 0, x >= 0], [lambda x: -x, lambda x: x])


    # send CV to VCA
    def process(self, t, sample_size, gate, attack, decay, sustain, release):
        t = (np.arange(sample_size) + t - self.t_press) / self.sample_rate

        if gate > 0:
            out_data = self.attack() + self.decay() + self.sustain()
        else:
            out_data = self.release() # ??


        # https://dsp.stackexchange.com/questions/2555/help-with-equations-for-exponential-adsr-envelope


        return out_data