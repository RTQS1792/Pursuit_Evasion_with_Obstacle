import matplotlib.patches as patches
import numpy as np

class Evader:
    def __init__(self, position: list = [0, 0], speed: float = 0.1) -> None:
        """
        This is the constructor of the class Evader

        Parameters
        ----------
        position : list, optional
            the initial position of the Evader, by default [0, 0]
        speed : float, optional
            the speed of the Evader, by default 0.1
        """
        self.position = np.array(position, dtype=float)
        self.speed = speed
        self.color = 'red'
        self.shape = 'triangle'
        self.trajectory = [self.position.copy()]
        self.tangent_lines = None
    
    def __str__(self) -> str:
        """
        Returns a string representation of the Evader

        Returns
        -------
        str
            the string representation of the Evader
        """
        return f'Evader at {self.position} with speed {self.speed}'
    
    def draw(self, ax) -> None:
        """
        Draw the Evader on the given ax

        Parameters
        ----------
        ax : _type_
            the axis to draw the Evader on
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

if __name__ == '__main__':
    evader = Evader([0, 0], 0.1)
    print(evader)