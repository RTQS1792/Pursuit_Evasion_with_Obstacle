### Standard library imports ###
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

### Self defined imports ###
from pursuer import Pursuer
from evader import Evader
from obstacle import Obstacle
from utility import *

class GameBoard:
    def __init__(self, pursuer, evader, obstacle, board_size: int = 30, compute_isocrones: bool = True) -> None:
        """
        Initialize the GameBoard with pursuer, evader, obstacle, and board size.
        
        Parameters
        ----------
        pursuer : Pursuer
            The pursuer object
        evader : Evader
            The evader object
        obstacle : Obstacle
            The obstacle object
        board_size : int, optional
            Size of the game board, by default 30
        compute_isocrones : bool, optional
            Whether to compute isochrones on initialization, by default True
        """
        self.pursuer = pursuer
        self.evader = evader
        self.obstacle = obstacle
        self.board_size = board_size
        
        # Initialize grid with default values
        self.grid = {(x, y): [0.0, 0.0, 0.0] for x in np.arange(-self.board_size, self.board_size + 0.2, 0.2) 
                     for y in np.arange(-self.board_size, self.board_size + 0.2, 0.2)}
        self.isocrones = []
        
        # Compute isochrones if specified
        if compute_isocrones:
            self.compute_isocrones()

    def __str__(self) -> str:
        """
        Return a string representation of the GameBoard

        Returns
        -------
        str
            String representation of the GameBoard
        """
        return "\n".join(["Game board:", f"Pursuer: {self.pursuer}", f"Evader: {self.evader}", 
                          f"Obstacle: {self.obstacle}", f"Size: {self.board_size}"])
    
    def compute_isocrones(self, tolarance: float = 0.004)-> None:
        """
        Compute isochrones for the current game state.
        
        Parameters
        ----------
        tolarance : float, optional
            Tolerance for considering a point as part of the isochrone, by default 0.004
        """
        # Calculate total iterations for progress bar
        x_range = np.arange(-self.board_size, self.board_size + 0.1, 0.1)
        y_range = np.arange(-self.board_size, self.board_size + 0.1, 0.1)
        total_iterations = len(x_range) * len(y_range)

        # Create progress bar
        with tqdm(total=total_iterations, desc="Computing Isochrones", ncols=100) as pbar:
            for x in x_range:
                for y in y_range:
                    # Check if point is inside the obstacle
                    if np.hypot(x - self.obstacle.center[0], y - self.obstacle.center[1]) <= self.obstacle.radius:
                        self.grid[(x, y)] = [0.0, 0.0, self.board_size]
                    else:
                        # Compute distances for pursuer and evader
                        pursuer_distance = shortest_path_with_circle(self.obstacle.center, self.obstacle.radius, [x, y], self.pursuer.position)[0]
                        evader_distance = shortest_path_with_circle(self.obstacle.center, self.obstacle.radius, [x, y], self.evader.position)[0]
                        
                        # Store distances and time difference in grid
                        self.grid[(x, y)] = [pursuer_distance, evader_distance, 
                                             pursuer_distance * self.evader.speed - evader_distance * self.pursuer.speed]
                        
                        # If point is within tolerance, add to isochrones
                        if abs(self.grid[(x, y)][2]) <= tolarance:
                            self.isocrones.append([x, y])
                    
                    # Update progress bar
                    pbar.update(1)

        print("Isochrones computed")
        
    def update(self) -> None:
        # Move pursuer and evader to the next position
        # self.pursuer.move(self.evader.position)
        # self.evader.move(self.pursuer.position)
        pass
                    
    def draw(self) -> None:
        """
        Draw the current state of the game board, including pursuer, evader, obstacle, and isochrones.
        """
        fig, ax = plt.subplots()
        ax.set_xlim(-self.board_size, self.board_size)
        ax.set_ylim(-self.board_size, self.board_size)

        # Draw pursuer, evader, and obstacle
        self.pursuer.draw(ax, draw_vision=True)
        self.evader.draw(ax)
        self.obstacle.draw(ax)
        
        # Draw the isochrones if they exist
        if self.isocrones:
            isocrone_x, isocrone_y = zip(*self.isocrones)
            ax.scatter(isocrone_x, isocrone_y, c='red', s=0.05, label='Isochrone')

        plt.gca().set_aspect("equal", adjustable="box")
        plt.show()


if __name__ == "__main__":
    # Set up the game board
    board_size = 40
    obstacle = Obstacle([0, 0], "circle", 5, "green")
    pursuer = Pursuer([6, -10], 0.1, board_size=board_size, obstacle=obstacle)
    evader = Evader([0, 10], 0.05, board_size=board_size, obstacle=obstacle)
    
    # Create and draw the game board
    game_board = GameBoard(pursuer, evader, obstacle, board_size)
    print(game_board)
    game_board.draw()