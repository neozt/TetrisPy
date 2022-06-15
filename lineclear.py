from dataclasses import dataclass

LINES_TO_WORD = {1: 'Single', 2: 'Double', 3: 'Triple', 4: 'Tetris'}


@dataclass(frozen=True)
class LineClear:
    lines: int
    tspin: bool

    @property
    def score(self):
        if self.tspin:
            send = 2 * self.lines
        else:
            if self.lines == 4:
                send = 4
            else:
                send = self.lines - 1
        return send * 100

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
