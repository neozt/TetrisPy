from game import Game
from board import Board

class View:
    def update(self, game: Game, update_type: str = 'normal'):
        if update_type == 'line clear':
            self.render_line_clear(game)
        elif update_type == 'death':
            self.render_death(game)
        else:
            self.render_game(game)

    def render_game(self, game: Game):
        print(game.current_mino)
        print(game.board)

    def render_line_clear(self, game: Game):
        print(game.total_clears[-1])
        self.render_game(game)

    def render_death(self, game: Game):
        print("GAME OVER")
        self.render_game(game)