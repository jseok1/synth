class Module:

    def __init__(self) -> None:
        self.config = {}

    def process(self, signal):
        raise NotImplementedError()
    
