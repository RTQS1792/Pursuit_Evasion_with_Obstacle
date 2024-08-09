import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from matplotlib import animation

from pursuer import Pursuer
from evader import Evader
from obstacle import Obstacle
from utility import shortest_path_with_circle

class GameBoard:
    def __init__(self, pursuer: Pursuer, evader: Evader, obstacle: Obstacle, board_size: int = 30, compute_isochrones: bool = True) -> None:
        """
        Initialize the GameBoard with pursuer, evader, obstacle, and board size.
        
        Parameters:
        - pursuer (Pursuer): The pursuer object
        - evader (Evader): The evader object
        - obstacle (Obstacle): The obstacle object
        - board_size (int): Size of the game board (default: 30)
        - compute_isochrones (bool): Whether to compute isochrones on initialization (default: True)
        """
        self.pursuer = pursuer
        self.evader = evader
        self.obstacle = obstacle
        self.board_size = board_size
        
        # Initialize grid with default values
        self.grid = {(x, y): [0.0, 0.0, 0.0] for x in np.arange(-self.board_size, self.board_size + 0.2, 0.2) 
                     for y in np.arange(-self.board_size, self.board_size + 0.2, 0.2)}
        self.isochrones = []
        
        self.fig, self.ax = plt.subplots()
        
        # Compute isochrones if specified
        if compute_isochrones:
            self.compute_isochrones()

    def __str__(self) -> str:
        """Return a string representation of the GameBoard"""
        return "\n".join([
            "Game board:",
            f"Pursuer: {self.pursuer}",
            f"Evader: {self.evader}", 
            f"Obstacle: {self.obstacle}",
            f"Size: {self.board_size}"
        ])
    
    def compute_isochrones(self, tolerance: float = 0.004) -> None:
        """
        Compute isochrones for the current game state.
        
        Parameters:
        - tolerance (float): Tolerance for considering a point as part of the isochrone (default: 0.004)
        """
        x_range = np.arange(-self.board_size, self.board_size + 0.1, 0.1)
        y_range = np.arange(-self.board_size, self.board_size + 0.1, 0.1)
        total_iterations = len(x_range) * len(y_range)

        with tqdm(total=total_iterations, desc="Computing Isochrones", ncols=100) as pbar:
            for x in x_range:
                for y in y_range:
                    if np.hypot(x - self.obstacle.center[0], y - self.obstacle.center[1]) <= self.obstacle.radius:
                        self.grid[(x, y)] = [0.0, 0.0, self.board_size]
                    else:
                        pursuer_distance, _ = shortest_path_with_circle(self.obstacle.center, self.obstacle.radius, [x, y], self.pursuer.position)
                        evader_distance, _ = shortest_path_with_circle(self.obstacle.center, self.obstacle.radius, [x, y], self.evader.position)
                        
                        time_difference = pursuer_distance * self.evader.speed - evader_distance * self.pursuer.speed
                        self.grid[(x, y)] = [pursuer_distance, evader_distance, time_difference]
                        
                        if abs(time_difference) <= tolerance:
                            self.isochrones.append([x, y])
                    
                    pbar.update(1)

        print("Isochrones computed")
        
    def update(self) -> None:
        """Update the positions of pursuer and evader"""
        self.pursuer.move_shortest_path(self.evader.position)
        self.evader.move_opposite_direction(self.pursuer.position)
    
    def draw_frame(self) -> None:
        """Draw the current state of the game board"""
        self.ax.clear()
        self.ax.set_xlim(-self.board_size, self.board_size)
        self.ax.set_ylim(-self.board_size, self.board_size)

        # Draw pursuer, evader, and obstacle
        self.pursuer.draw(self.ax, draw_vision=True)
        self.evader.draw(self.ax)
        self.obstacle.draw(self.ax)
        
        # Draw pursuer's trajectory
        pursuer_trajectory = np.array(self.pursuer.trajectory)
        print(pursuer_trajectory)
        self.ax.plot(pursuer_trajectory[:, 0], pursuer_trajectory[:, 1], color=self.pursuer.color, linestyle='--', linewidth=1)

        # Draw evader's trajectory
        evader_trajectory = np.array(self.evader.trajectory)
        self.ax.plot(evader_trajectory[:, 0], evader_trajectory[:, 1], color=self.evader.color, linestyle='--', linewidth=1)

        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_title(f'Frame {self.frame_num}')

    def animate_func(self, frame):
        """Animation function to be called for each frame"""
        self.frame_num = frame
        self.update()
        self.draw_frame()
        return self.ax.patches  # Return the updated patches for blitting

    def animate(self, num_frames: int = 400, interval: int = 50) -> None:
        """
        Create and display the animation
        
        Parameters:
        - num_frames (int): Number of frames in the animation (default: 200)
        - interval (int): Interval between frames in milliseconds (default: 50)
        """
        self.frame_num = 0
        self.pbar = tqdm(total=num_frames, desc="Animating", ncols=100)
        
        anim = animation.FuncAnimation(
            self.fig, self.animate_func, frames=num_frames, interval=interval, blit=False
        )

        plt.show(block=True)
        self.pbar.close()
                    
    def draw(self) -> None:
        """Draw the current state of the game board, including pursuer, evader, obstacle, and isochrones."""
        fig, ax = plt.subplots()
        ax.set_xlim(-self.board_size, self.board_size)
        ax.set_ylim(-self.board_size, self.board_size)

        # Draw pursuer, evader, and obstacle
        self.pursuer.draw(ax, draw_vision=True)
        self.evader.draw(ax)
        self.obstacle.draw(ax)
        
        # Draw the isochrones if they exist
        if self.isochrones:
            isochrone_x, isochrone_y = zip(*self.isochrones)
            ax.scatter(isochrone_x, isochrone_y, c='red', s=0.05, label='Isochrone')

        plt.gca().set_aspect("equal", adjustable="box")
        plt.show()


if __name__ == "__main__":
    # Set up the game board
    board_size = 40
    obstacle = Obstacle([0, 0], 5, "circle", "green")
    pursuer = Pursuer([6, -10], 0.1, board_size=board_size, obstacle=obstacle)
    evader = Evader([0, 10], 0.05, board_size=board_size, obstacle=obstacle)
    
    # Create and animate the game board
    game_board = GameBoard(pursuer, evader, obstacle, board_size, compute_isochrones=False)
    print(game_board)
    game_board.animate(num_frames=200, interval=20)