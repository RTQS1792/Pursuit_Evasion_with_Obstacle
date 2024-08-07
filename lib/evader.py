### Standard library imports ###
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

### Self defined imports ###
from obstacle import Obstacle
from utility import compute_tangents_circle

class Evader:
    def __init__(self, position: list = [0, 0], speed: float = 0.1, board_size: int = 15, 
                 obstacle: Obstacle = Obstacle([0, 0], "circle", 5, "green")) -> None:
        """
        Constructor for the Evader class

        Args:
        -----
        position (list): Initial position of the Evader. Default is [0, 0].
        speed (float): Speed of the Evader. Default is 0.1.
        board_size (int): Size of the game board. Default is 15.
        obstacle (Obstacle): Obstacle object. Default is a green circle at [0, 0] with radius 5.

        Returns:
        --------
        None
        """
        self.position = np.array(position, dtype=float)
        self.speed = speed
        self.board_size = board_size
        self.color = 'red'
        self.shape = 'triangle'
        self.trajectory = [self.position.copy()]
        self.obstacle = obstacle

        # Compute tangent points and lines
        tangents = compute_tangents_circle(self.obstacle.center, self.obstacle.radius, self.position)
        self.tangent_points = tangents[:2]
        self.tangent_lines = tangents[2:]
    
    def __str__(self) -> str:
        """
        Returns a string representation of the Evader

        Returns:
        --------
        str: String representation of the Evader
        """
        return f'Evader at {self.position} with speed {self.speed}'
    
    def draw(self, ax) -> None:
        """
        Draw the Evader on the given axis

        Args:
        -----
        ax (matplotlib.axes.Axes): The axis to draw on

        Returns:
        --------
        None
        """
        self.patch = patches.RegularPolygon(
            self.trajectory[0],  # position
            numVertices=3,
            radius=0.5,  # size of the triangle
            orientation=np.pi / 2,  # point facing up
            facecolor=self.color,
            edgecolor='black',
            lw=2,
            alpha=0.5,
        )
        ax.add_patch(self.patch)

if __name__ == "__main__":
    # Create figure and axis
    fig, ax = plt.subplots()

    # Create obstacle and evader
    obstacle = Obstacle([0, 0], "circle", 5, "green")
    evader = Evader([0, 10], 0.1, obstacle=obstacle)

    # Draw evader and obstacle
    evader.draw(ax)
    obstacle.draw(ax)

    # Set plot limits and aspect ratio
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    plt.gca().set_aspect("equal", adjustable="box")

    # Show the plot
    plt.show()