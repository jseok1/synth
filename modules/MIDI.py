class MIDI:

    # not really MIDI right now
    def __init__(self) -> None:
        pass

    def note_to_cv(self, note):
        assert 0 <= note <= 127

        # MIDI is 0-127 (C-1 to G9)
        # octave C D E F G A B
        # 1 V/OCT

        # Let's say C-1 is 0V

        return note / 12
    
        # then f = f0 x 2^(V - V0) , where f0 is C-1 and V0 is 0
