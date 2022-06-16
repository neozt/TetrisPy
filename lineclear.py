from dataclasses import dataclass

LINES_TO_WORD = {1: 'Single', 2: 'Double', 3: 'Triple', 4: 'Tetris'}


@dataclass(frozen=True)
class LineClear:
    lines: int
    tspin: bool

    @property
    def score(self):
        match (self.lines, self.tspin):
            case (_, True):
                # Tspins are worth double the lines sent
                send = 2 * self.lines
            case (1, False):
                # Single is worth very little
                send = 0.01
            case (4, False):
                # Tetrises are worth 4
                send = 4
            case (_, False):
                # Doubles and Triples are worth 1 and 2 points resp.
                send = self.lines - 1
        return int(send * 100)

    @property
    def string(self):
        t_spin_string = 'T-Spin ' if self.tspin else ''
        return t_spin_string + LINES_TO_WORD.get(self.lines)

    @property
    def abbreviation(self):
        abbreviation = ''
        if self.tspin:
            if self.lines == 1:
                abbreviation = 'TSS'
            elif self.lines == 2:
                abbreviation = 'TSD'
            elif self.lines == 3:
                abbreviation = 'TST'
        else:
            abbreviation = self.string
        return abbreviation
