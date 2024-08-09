### Standard library imports ###
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

### Self defined imports ###
from obstacle import Obstacle
from utility import *

class Evader:
    def __init__(self, position: list = [0, 0], speed: float = 0.1, board_size: int = 15, 
                 obstacle: Obstacle = Obstacle([0, 0], 5, "circle", "green")) -> None:
        """
        Constructor for the Evader class

        Parameters
        ----------
        position : list, optional
            Initial position of the Evader, by default [0, 0]
        speed : float, optional
            Speed of the Evader, by default 0.1
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
        self.color = 'red'
        self.shape = 'triangle'
        self.trajectory = [self.position.copy()]
        self.obstacle = obstacle

    def move(self, pursuer_position: np.array) -> None:
        """
        Move the Evader based on the visibility of the pursuer

        Parameters
        ----------
        pursuer_position : np.array
            The position of the pursuer

        Returns
        -------
        None
        """
        # Check if there's line of sight between evader and pursuer
        line_of_sight = not does_line_intersect_circle(
            self.position, pursuer_position, 
            self.obstacle.center, self.obstacle.radius
        )

        if line_of_sight:
            # If there's line of sight, move away from the pursuer
            self.move_opposite_direction(pursuer_position)
        else:
            # If there's no line of sight, move along the tangent line
            self.move_along_tangent(pursuer_position)

    def move_opposite_direction(self, pursuer_position: np.array) -> None:
        """
        Move the Evader in the opposite direction of the pursuer

        Parameters
        ----------
        pursuer_position : np.array
            The position of the pursuer

        Returns
        -------
        None
        """
        direction = self.position - pursuer_position
        new_position = self.position + self.speed * direction / np.linalg.norm(direction)
        
        # Check if the new position is within the board boundaries
        if np.all(np.abs(new_position) <= self.board_size):
            self.position = new_position
        
        self.trajectory.append(self.position.copy())

    def move_along_tangent(self, pursuer_position: np.array) -> None:
        """
        Move the Evader along the tangent line away from the pursuer

        Parameters
        ----------
        pursuer_position : np.array
            The position of the pursuer

        Returns
        -------
        None
        """
        # Compute tangent points and lines
        tangents = compute_tangents_circle(self.obstacle.center, self.obstacle.radius, self.position)
        tangent_points = tangents[:2]
        
        # Determine which tangent point is further from the pursuer
        distances = [np.linalg.norm(np.array(point) - pursuer_position) for point in tangent_points]
        further_tangent = tangent_points[np.argmax(distances)]
        
        # Calculate direction vector along the tangent line
        direction = np.array(further_tangent) - self.position
        
        # Move along the tangent line
        new_position = self.position + self.speed * direction / np.linalg.norm(direction)
        
        # Check if the new position is within the board boundaries
        if np.all(np.abs(new_position) <= self.board_size):
            self.position = new_position
        
        self.trajectory.append(self.position.copy())

    def draw(self, ax) -> None:
        """
        Draw the Evader on the given axis

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis to draw on

        Returns
        -------
        None
        """
        self.patch = patches.RegularPolygon(
            self.position,  # Use current position
            numVertices=3,
            radius=0.5,  # size of the triangle
            orientation=np.pi / 2,  # point facing up
            facecolor=self.color,
            edgecolor='black',
            lw=2,
            alpha=0.5,
        )
        ax.add_patch(self.patch)

    def __str__(self) -> str:
        """
        Returns a string representation of the Evader

        Returns
        -------
        str
            String representation of the Evader
        """
        return f'Evader at {self.position} with speed {self.speed}'