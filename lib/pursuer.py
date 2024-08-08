### Standard library imports ###
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from shapely.geometry import Polygon

### Self defined imports ###
from obstacle import Obstacle
from utility import *

class Pursuer:
    def __init__(self, position: list = [0, 0], speed: float = 0.1, board_size: int = 15, 
                 obstacle: Obstacle = Obstacle([0, 0], "circle", 5, "green")) -> None:
        """
        Constructor for the Pursuer class

        Parameters
        ----------
        position : list, optional
            Initial position of the Pursuer, by default [0, 0]
        speed : float, optional
            Speed of the Pursuer, by default 0.1
        board_size : int, optional
            Size of the game board, by default 15
        obstacle : Obstacle, optional
            Obstacle object, by default a green circle at [0, 0] with radius 5

        Returns
        -------
        None
        """
        self.position = np.array(position, dtype=float)
        self.speed = speed
        self.board_size = board_size
        self.color = "blue"
        self.shape = "circle"
        self.trajectory = [self.position.copy()]
        self.obstacle = obstacle
        
        # Compute tangent points and lines
        tangents = compute_tangents_circle(self.obstacle.center, self.obstacle.radius, self.position)
        self.tangent_points = tangents[:2]
        self.tangent_lines = tangents[2:]

    def __str__(self) -> str:
        """
        Returns a string representation of the Pursuer

        Returns
        -------
        str
            String representation of the Pursuer
        """
        return f"Pursuer at {self.position} with speed {self.speed}"

    def draw(self, ax, draw_vision: bool = False, draw_trajectory: bool = False) -> None:
        """
        Draw the Pursuer on the given axis

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis to draw on
        draw_vision : bool, optional
            Whether to draw the Pursuer's vision, by default False
        draw_trajectory : bool, optional
            Whether to draw the Pursuer's trajectory, by default False

        Returns
        -------
        None
        """
        # Draw Pursuer
        self.patch = patches.Circle(
            self.position,
            0.5,
            facecolor=self.color,
            edgecolor="black",
            lw=2,
            alpha=0.5,
        )
        ax.add_patch(self.patch)

        # Draw vision if requested
        if draw_vision:
            self._draw_vision(ax)

        # TODO: Implement draw_trajectory functionality
        if draw_trajectory:
            pass  # Not implemented yet

    def _draw_vision(self, ax) -> None:
        """
        Draw the Pursuer's vision on the given axis

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis to draw on

        Returns
        -------
        None
        """
        # Define the corners of the game board
        graph_corners = [(-self.board_size, -self.board_size), (-self.board_size, self.board_size), 
                         (self.board_size, self.board_size), (self.board_size, -self.board_size)]
        plotting_area = Polygon(graph_corners)

        # Extract tangent line points
        (p1, t1), (p2, t2) = self.tangent_lines

        # Create a polygon representing the blocked area
        blocked_area = Polygon([p1, p2, t1, t2])

        # Calculate the vision area
        vision_area = plotting_area.difference(blocked_area)

        # Draw the vision area
        patch = patches.Polygon(list(vision_area.exterior.coords), closed=True, fill=True, color="grey", alpha=0.3)
        ax.add_patch(patch)


if __name__ == "__main__":
    # Create figure and axis
    fig, ax = plt.subplots()

    # Create obstacle and pursuer
    obstacle = Obstacle([0, 0], "circle", 5, "green")
    pursuer = Pursuer([0, -10], 0.1, obstacle=obstacle)

    # Draw pursuer and obstacle
    pursuer.draw(ax, draw_vision=True)
    obstacle.draw(ax)

    # Set plot limits and aspect ratio
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    plt.gca().set_aspect("equal", adjustable="box")

    # Show the plot
    plt.show()