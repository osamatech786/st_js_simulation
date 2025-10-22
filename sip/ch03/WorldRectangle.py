import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ****************************************
# WorldRectangle Class
# ****************************************
class WorldRectangle:
    """
    WorldRectangle stores the properties of a rectangle in world coordinates 
    and provides a method to draw it on a Matplotlib plot.
    """
    def __init__(self, left, top, width, height):
        """
        Constructs a WorldRectangle with position and dimensions in world coordinates.
        
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
