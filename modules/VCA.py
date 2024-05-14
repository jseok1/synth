import numpy as np


class VCA:

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate

    def process(self, sample_size, in_data, level, level_cv=1):
        out_data = in_data * level * level_cv
        return out_data
