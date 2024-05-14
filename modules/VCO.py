import numpy as np

from modules.LFO import LFO

# it's a graph traversal technically using topological sort
lfo = LFO(44100)

class VCO:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate
        self.config = {
            'WAVE': 'sine',
            # 'FREQ': 16.35 * np.ones(shape=(frame_count,)),  # this can be modulated (LFO) or interpolated (manual change),
            # 'FM': np.ones(shape=(frame_count,)),
            # 'OCT': np.ones(shape=(frame_count))
        }
        self.shift = 0

    # envelope need press and release times
    # can store in milliseconds relative to the time process() is called
    # so is negative

    # square wave is easy to implement using sign(sin(x))


    # idea: always keep buffer ending at 0 so the next one starts at 0?
    # or keep phase shift <-- preferred.
    def process(self, t, sample_size, voltage):
        frequency = 8.175799 * 2 ** voltage  # C-1 for reference
        # t = frequency * (np.arange(sample_size) + t) / self.sample_rate
        

        # frequency = A + (B - A) * np.arange(frame_count)
        t = lfo.process(t, sample_size)

        # frequency = self.config['FREQ']
        if self.config['WAVE'] == 'sine':
            out_data = np.sin(2 * np.pi * t)
        elif self.config['WAVE'] == 'square':
            out_data = np.sign(np.sin(2 * np.pi * t))
        elif self.config['WAVE'] == 'triangle':
            out_data = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * t))
        elif self.config['WAVE'] == 'saw':
            out_data = 1 / np.pi * np.arctan(np.tan(np.pi * t))


        # out_data *= self.config['V/OCT']

        # LFO actually outputs its integral, which can be split up by time, i.e
        # 0 to t_prev + t_prev to t



        return out_data.astype(np.float32)
    

    # def wave():
    #     signal.sawtooth(2 * np.pi * freq * t)
    #     signal.square(2 * np.pi * freq * t)
    #     signal.sawtooth(2 * np.pi * freq * t, width=0.5) # triangle


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    frame_count = 576
    vco = VCO(44100)

    t = 0

    # out_data1 = lfo.process(t, frame_count)
    out_data1 = vco.process(t, frame_count, 5)
    plt.figure()
    plt.plot((np.arange(frame_count) + t) / 44100, out_data1)
    plt.show()

    t = 576

    # out_data2 = lfo.process(t, frame_count)
    out_data2 = vco.process(t, frame_count, 5)
    plt.figure()
    plt.plot((np.arange(frame_count) + t) / 44100, out_data2)
    plt.show()    


    plt.figure()
    plt.plot(
        np.concatenate([(np.arange(frame_count) + 0) / 44100, (np.arange(frame_count) + 576) / 44100]),
        np.concatenate([out_data1, out_data2]))
    plt.show() 

    # https://stackoverflow.com/questions/26028763/how-to-change-parameters-realtimely-in-portaudio