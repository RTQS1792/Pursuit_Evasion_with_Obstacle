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
    
    def move_shortest_path(self, evader_position: np.array) -> None:
        # Check if the evader is in sight
        if not does_line_intersect_circle(self.position, evader_position, self.obstacle.center, self.obstacle.radius):
            # Evader is in sight, move directly towards it
            direction = evader_position - self.position
            direction = direction / np.linalg.norm(direction)
            new_position = self.position + direction * self.speed
        else:
            # Evader is out of sight
            distance_to_obstacle = np.linalg.norm(self.position - self.obstacle.center) - self.obstacle.radius
            
            if distance_to_obstacle > 1e-6:  # Not on the circle edge
                # Move towards the right tangent point
                right_tangent = self.tangent_points[1]  # Assuming the second point is the right tangent
                direction = right_tangent - self.position
                direction = direction / np.linalg.norm(direction)
                new_position = self.position + direction * self.speed
            else:  # On the circle edge
                # Move counterclockwise along the edge
                angle = np.arctan2(self.position[1] - self.obstacle.center[1], 
                                   self.position[0] - self.obstacle.center[0])
                new_angle = angle + self.speed / self.obstacle.radius
                new_position = self.obstacle.center + self.obstacle.radius * np.array([np.cos(new_angle), np.sin(new_angle)])

        # Update position and trajectory
        self.position = new_position
        self.trajectory.append(self.position.copy())

        # Recompute tangent points and lines
        tangents = compute_tangents_circle(self.obstacle.center, self.obstacle.radius, self.position)
        self.tangent_points = tangents[:2]
        self.tangent_lines = tangents[2:]
            

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

        # Extract tangent line points
        (p1, t1), (p2, t2) = self.tangent_lines

        # Calculate angles for the tangent lines
        angle_t1 = calculate_angle(t1, p1)
        angle_t2 = calculate_angle(t2, p1)
        
        # Ensure angle_t1 < angle_t2
        if angle_t1 > angle_t2:
            angle_t1, angle_t2 = angle_t2, angle_t1

        # Add tangent points to the vision polygon
        vision_polygon_points = [p1, t1, t2, p2]

        # Check each corner to see if it should be included
        for corner in graph_corners:
            angle_corner = calculate_angle(corner, p1)
            # Check if corner's angle is between angle_t1 and angle_t2
            if angle_t1 <= angle_corner <= angle_t2:
                vision_polygon_points.append(corner)

        print(vision_polygon_points)
        
        # Sort points counter-clockwise to form a valid polygon
        vision_polygon_points = sorted(vision_polygon_points, key=lambda point: calculate_angle(point, p1))
        
        # Draw the vision area
        patch = patches.Polygon(list(Polygon(vision_polygon_points).exterior.coords), closed=True, fill=True, color="grey", alpha=0.3)
        ax.add_patch(patch)


if __name__ == "__main__":
    # Create figure and axis
    fig, ax = plt.subplots()

    # Create obstacle and pursuer
    obstacle = Obstacle([0, 0], 5, "circle", "green")
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