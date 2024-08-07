import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Obstacle:
    def __init__(self, center: list = [0, 0], shape: str = "circle", radius: float = 5, color: str = "green") -> None:
        """
        This is the constructor for the Obstacle class

        Parameters
        ----------
        center : list, optional
            the center of the Obstacle, by default [0,0]
        radius : float, optional
            the radius of the Obstacle if it is a circle, by default 5
        shape : str, optional
            the shape of the Obstacle, by default "circle"
        color : str, optional
            the color of the Obstacle, by default "green"
        """
        self.center = center
        self.radius = radius
        self.shape = shape
        self.color = color

    def __str__(self) -> str:
        """
        Returns a string representation of the Obstacle

        Returns
        -------
        str
            the string representation of the Obstacle
        """
        return f"Obstacle: center={self.center}, shape={self.shape}, color={self.color}"

    def draw(self, ax) -> None:
        if self.shape == "circle":
            circle = patches.Circle(
                self.center,
                self.radius,
                facecolor=self.color,
                edgecolor="black",
                lw=1,
                alpha=0.5,
            )
            ax.add_patch(circle)
        else:
            raise ValueError(f"Unsupported shape: {self.shape}")


if __name__ == "__main__":
    fig, ax = plt.subplots()
    obstacle = Obstacle([0, 0], "circle", 5, "green")
    obstacle.draw(ax)
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()
