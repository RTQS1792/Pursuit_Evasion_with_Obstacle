from pursuer import Pursuer
from evader import Evader
from obstacle import Obstacle
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np


class GameBoard:
    def __init__(self, pursuer, evader, obstacle, graph_size: int = 15):
        self.pursuer = pursuer
        self.evader = evader
        self.obstacle = obstacle
        self.graph_size = graph_size
        self.grid = {(x, y): [0.0, 0.0, 0.0] for x in np.arange(-self.size, self.size + 0.1, 0.1) for y in np.arange(-self.size, self.size + 0.1, 0.1)}

    def __str__(self):
        return "\n".join(["Game board:", f"Pursuer: {self.pursuer}", f"Evader: {self.evader}", f"Obstacle: {self.obstacle}", f"Size: {self.size}"])

    def draw(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-self.size, self.size)
        ax.set_ylim(-self.size, self.size)

        self.pursuer.draw(ax)
        self.evader.draw(ax)
        self.obstacle.draw(ax)

        plt.gca().set_aspect("equal", adjustable="box")
        plt.show()


if __name__ == "__main__":
    obstacle = Obstacle([0, 0], "circle", 5, "green")
    pursuer = Pursuer([0, -10], 0.1, obstacle=obstacle)
    evader = Evader([0, 10], 0.1, obstacle=obstacle)
    graph_size = 15
    game_board = GameBoard(pursuer, evader, obstacle, graph_size)
    print(game_board)
