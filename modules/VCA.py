import numpy as np


class VCA:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate

    def process(self, in_data, level):
        out_data = in_data * level
        return out_data
