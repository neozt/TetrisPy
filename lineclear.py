from dataclasses import dataclass

@dataclass
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