from dataclasses import dataclass

from mino import Mino
import mino as mn

class HoldDisabledException(Exception):
    pass

@dataclass
class Hold:
    held_mino: Mino = None
    allow_hold: bool = True

    def hold_mino(self, mino: Mino) -> Mino | None:
        # Handle first hold event specailly since there is no mino to be returned
        if self.held_mino is None:
            self.held_mino = mino
            self.disable_hold()
            return None

        if self.allow_hold:
            held_mino = mn.create_mino(self.held_mino.type)  # Create a new copy of the same mino type so that it spawns in the default position
            self.held_mino = mino   # Replace outgoing mino with new mino
            self.disable_hold()     # Disable hold until returned mino is place to prevent indefinite cycling between held minos
            return held_mino
        else:
            raise HoldDisabledException('Currently not allowed to hold')

    def enable_hold(self) -> None:
        self.allow_hold = True

    def disable_hold(self) -> None:
        self.allow_hold = False
