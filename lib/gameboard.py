from pursuer import Pursuer
from evader import Evader
from obstacle import Obstacle
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
from utility import *
from tqdm import tqdm


class GameBoard:
    def __init__(self, pursuer, evader, obstacle, board_size: int = 30):
        self.pursuer = pursuer
        self.evader = evader
        self.obstacle = obstacle
        self.board_size = board_size
        self.grid = {(x, y): [0.0, 0.0, 0.0] for x in np.arange(-self.board_size, self.board_size + 0.1, 0.1) for y in np.arange(-self.board_size, self.board_size + 0.1, 0.1)}
        self.isocrones = []
        self.compute_isocrones()

    def __str__(self):
        return "\n".join(["Game board:", f"Pursuer: {self.pursuer}", f"Evader: {self.evader}", f"Obstacle: {self.obstacle}", f"Size: {self.board_size}"])
    
    def compute_isocrones(self):
        # Calculate total iterations
        x_range = np.arange(-self.board_size, self.board_size + 0.1, 0.1)
        y_range = np.arange(-self.board_size, self.board_size + 0.1, 0.1)
        total_iterations = len(x_range) * len(y_range)

        # Create progress bar
        with tqdm(total=total_iterations, desc="Computing Isochrones") as pbar:
            for x in x_range:
                for y in y_range:
                    # Check if point is inside the obstacle
                    if np.hypot(x - self.obstacle.center[0], y - self.obstacle.center[1]) <= self.obstacle.radius:
                        self.grid[(x, y)] = [0.0, 0.0, self.board_size]
                    else:
                        pursuer_distance = shortest_path_with_circle(self.obstacle.center, self.obstacle.radius, [x, y], self.pursuer.position)[0]
                        evader_distance = shortest_path_with_circle(self.obstacle.center, self.obstacle.radius, [x, y], self.evader.position)[0]
                        self.grid[(x, y)] = [pursuer_distance, evader_distance, pursuer_distance * self.evader.speed - evader_distance * self.pursuer.speed]
                        if abs(self.grid[(x, y)][2]) <= 0.005:
                            self.isocrones.append([x, y])
                    
                    # Update progress bar
                    pbar.update(1)

        print("Isochrones computed")
    
    def draw(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-self.board_size, self.board_size)
        ax.set_ylim(-self.board_size, self.board_size)

        self.pursuer.draw(ax, draw_vision=True)
        self.evader.draw(ax)
        self.obstacle.draw(ax)
        
        # Draw the isochrones
        if self.isocrones:
            isocrone_x, isocrone_y = zip(*self.isocrones)
            ax.scatter(isocrone_x, isocrone_y, c='red', s=0.1, label='Isochrone')

        plt.gca().set_aspect("equal", adjustable="box")
        plt.show()


if __name__ == "__main__":
    board_size = 40
    obstacle = Obstacle([0, 0], "circle", 5, "green")
    pursuer = Pursuer([6, -10], 0.1, board_size=board_size, obstacle=obstacle)
    evader = Evader([0, 10], 0.05, board_size=board_size, obstacle=obstacle)
    game_board = GameBoard(pursuer, evader, obstacle, board_size)
    print(game_board)
    game_board.draw()