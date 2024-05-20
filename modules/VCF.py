import numpy as np
import scipy.signal as signal
import time


class VCF:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate
        self.order = 2
        self.out_data_prev = np.zeros((576,))
        self.in_data_prev = np.zeros((576,))

    def butter(self, normalized_cutoff):
        b, a = signal.butter(2, normalized_cutoff, 'low')
        return b, a

    # IIR
    def process(self, sample_size, in_data, freq_cut, res):
        # https://stackoverflow.com/questions/20924868/calculate-coefficients-of-2nd-order-butterworth-low-pass-filter

        # IIR
        out_data = np.zeros((2 * sample_size,))
        out_data[:sample_size] = self.out_data_prev
        in_data_ = np.concatenate((self.in_data_prev, in_data))
        for i in range(sample_size, 2 * sample_size):
            k = np.tan(np.pi * freq_cut / self.sample_rate)
            q = 1 / np.sqrt(2) + res

            norm = 1 + k / q + k * k

            b = np.array([k * k / norm,
                          2 * k * k / norm,
                          k * k / norm])
            a = np.array([1,
                          2 * (k * k - 1) / norm,
                          (1 - k / q + k * k) / norm])

            out_data[i] = np.dot(in_data_[i - 2:i + 1], b[::-1]) - np.dot(out_data[i - 2:i], a[:0:-1])
        out_data = out_data[sample_size:]

        self.in_data_prev = in_data
        self.out_data_prev = out_data
        return out_data


        # FIR
        nyquist = 0.5 * self.sample_rate
        normalized_cutoff = freq_cut / nyquist
        b = signal.firwin(101, normalized_cutoff, window='hamming')[::-1]

        in_data_ = np.concatenate((self.in_data_prev, in_data))

        out_data = np.zeros((sample_size,))
        for i in range(sample_size):
            out_data[i] = np.dot(in_data_[i - len(b) + sample_size + 1:i + sample_size + 1], b)

        self.in_data_prev = in_data
        return out_data


        # np.lib.stride_tricks.sliding_window_view(in_data, window_size)
        # 12 or 24 dB/Oct slope? (generally gentle slope)
        # 2 pole filters are most common (can control resonance, can be cascaded)
    


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    from VCO import VCO

    vco = VCO(44100)
    vcf = VCF(44100)

    t = 0
    data1 = vco.process(t, 576, 5, 1, 'saw')
    data2 = vcf.process(576, data1, 20 * 10 ** (3 * 0.3), 0.0)
    data3 = vcf.process(576, data1, 20 * 10 ** (3 * 0.3), 2.0)


    plt.figure()
    plt.plot(np.arange(576) / 44100, data1)
    plt.plot(np.arange(576) / 44100, data2)
    plt.plot(np.arange(576) / 44100, data3)
    plt.show()

    # TODO: ensure stability
    # plot 



    # from scipy import signal

    # fs = 1000  # Sampling frequency
    # # Generate the time vector properly
    # t = np.arange(1000) / fs
    # signala = np.sin(2*np.pi*100*t) # with frequency of 100
    # plt.plot(t, signala, label='a')

    # signalb = np.sin(2*np.pi*20*t) # frequency 20
    # plt.plot(t, signalb, label='b')

    # signalc = signala + signalb
    # plt.plot(t, signalc, label='c')

    # fc = 30  # Cut-off frequency of the filter
    # w = fc / (fs / 2) # Normalize the frequency
    # b, a = signal.butter(5, w, 'low')
    # output = signal.filtfilt(b, a, signalc)
    # plt.plot(t, output, label='filtered')
    # plt.legend()
    # plt.show()