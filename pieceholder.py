from dataclasses import dataclass

from mino import Mino
import mino

class NoHeldMinoException(Exception):
    pass

@dataclass
class Hold:
    held_mino: Mino = None
    allow_hold: bool = True

    def hold_mino(self, mino: Mino) -> Mino:
        if self.allow_hold:
            held_mino = mino.create_mino(self.held_mino.type)  # Create a new copy of the same mino type so that it spawns in the default position
            self.held_mino = mino   # Replace outgoing mino with new mino
            return held_mino
        else:
            raise NoHeldMinoException('Currently not allowed to hold')

    def enable_hold(self) -> None:
        self.allow_hold = True

    def disable_hold(self) -> None:
        self.allow_hold = False