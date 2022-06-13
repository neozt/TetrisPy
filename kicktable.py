SRS_NORMAL_KICKS = [
    [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)], # 0>>1
    [(0,0), (1,0), (1,-1), (0,2), (1,2)],     # 1>>0
    [(0,0), (1,0), (1,-1), (0,2), (1,2)],     # 1>>2
    [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)], # 2>>1
    [(0,0), (1,0), (1,1), (0,2), (1,-2)],     # 2>>3
    [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],  # 3>>2
    [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],  # 3>>0
    [(0,0), (1,0), (1,1), (0,2), (1,-2)],     # 0>>3
]

SRS_I_KICKS = [
    [(0,0), (-2,0), (1,0), (-2,-1), (1,2)], # 0>>1
    [(0,0), (2,0), (-1,0), (2,1), (-1,-2)], # 1>>0
    [(0,0), (-1,0), (2,0), (-1,2), (2,-1)], # 1>>2
    [(0,0), (1,0), (-2,0), (1,-2), (-2,1)], # 2>>1
    [(0,0), (2,0), (-1,0), (2,1), (-1,-2)], # 2>>3
    [(0,0), (-2,0), (1,0), (-2,-1), (1,2)], # 3>>2
    [(0,0), (1,0), (-2,0), (1,-2), (-2,1)], # 3>>0
    [(0,0), (-1,0), (2,0), (-1,2), (2,-1)], # 0>>3
]

class KickTable:
    def __init__(self, normal_table = SRS_NORMAL_KICKS, I_table = SRS_I_KICKS) -> None:
        self.normal_table = normal_table
        self.I_table = I_table

    def get_kicks(self, from_orientation: int, to_orientation: int, mino_type: str) -> list[tuple[int,int]]:
        if mino_type == 'I':
            kick_table = self.I_table
        else:
            kick_table = self.normal_table

        match (from_orientation, to_orientation):
            case (0,1): return kick_table[0]
            case (1,0): return kick_table[1]
            case (1,2): return kick_table[2]
            case (2,1): return kick_table[3]
            case (2,3): return kick_table[4]
            case (3,2): return kick_table[5]
            case (3,0): return kick_table[6]
            case (0,3): return kick_table[7]

        


