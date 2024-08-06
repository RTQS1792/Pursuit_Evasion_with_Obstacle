import matplotlib.patches as patches
import numpy as np

class Pursuer:
    def __init__(self, position: list = [0, 0], speed: float = 0.1) -> None:
        """
        Constructor for the Pursuer class

        Parameters
        ----------
        position : list, optional
            the initial position of the Pursuer, by default [0, 0]
        speed : float, optional
            the speed of the Pursuer, by default 0.1
        """
        self.position = np.array(position, dtype=float)
        self.speed = speed
        self.color = "blue"
        self.shape = "circle"
        self.trajectory = [self.position.copy()]
        self.tangent_lines = None
        self.tangent_point_1 = None
        self.tangent_point_2 = None

    def __str__(self) -> str:
        """
        Returns a string representation of the Pursuer

        Returns
        -------
        str
            the string representation of the Pursuer
        """
        return f"Pursuer at {self.position} with speed {self.speed}"

    def draw(self, ax) -> None:
        """
        Draw the Pursuer on the given ax

        Parameters
        ----------
        ax : _type_
            the axis to draw the Pursuer on
        """
        self.patch = patches.Circle(
            self.position,
            0.5,
            facecolor=self.color,
            edgecolor="black",
            lw=2,
            alpha=0.5,
        )
        ax.add_patch(self.patch)

if __name__ == "__main__":
    pursuer = Pursuer([0, -10], 0.1)
    print(pursuer)