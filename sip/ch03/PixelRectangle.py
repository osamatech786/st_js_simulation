import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ****************************************
# PixelRectangle Class
# ****************************************
class PixelRectangle:
    """
    PixelRectangle stores the properties of a rectangle and provides a method 
    to draw it on a Matplotlib plot. This class is designed for use in a 
    Python-based visualization environment.
    """
    def __init__(self, left, top, width, height):
        """
        Constructs a PixelRectangle with position and dimensions in pixel coordinates.
        
        :param left: The x-coordinate of the top-left corner.
        :param top: The y-coordinate of the top-left corner.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        """
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def draw(self, ax):
        """
        Draws the rectangle on a Matplotlib Axes object.
        
        :param ax: The Matplotlib Axes to draw on.
        """
        # Create a rectangle patch and add it to the plot
        rect = patches.Rectangle(
            (self.left, self.top), 
            self.width, 
            self.height, 
            facecolor='red'
        )
        ax.add_patch(rect)
