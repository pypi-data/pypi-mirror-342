# Import necessary libraries
import numpy as np
import plotly.graph_objects as go
from abc import ABC, abstractmethod


class GeometricAnimation(ABC):
    """Abstract base class for geometric animations."""
    
    @abstractmethod
    def __init__(self, frame_count:int=100, duration:int=50, scale:float=1.09):
        """Abstract param initializer"""
        self.n = frame_count
        self.duration = duration
        self.scale = scale
    
    @abstractmethod
    def _create_figure(self):
        """create the Plotly figure"""
        pass
    
    def show(self):
        """Displays the animation."""
        self._create_figure().show()


class GuiInterface:
    """Class to manage the user interface elements (buttons, slider) for animations."""
    
    def __init__(self, parent):
        """
        Initializes the GUI elements based on the parent animation's properties.

        Args:
            parent: The animation object that this GUI controls.
        """
        self.parent = parent # need size 
        self.play = {"label": "Play", "method": "animate", 
                    "args": [None, {"frame": {"duration": parent.duration, "redraw": True}, 
                                   "fromcurrent": True}]}
        self.pause = {"label": "Pause", "method": "animate", 
                     "args": [[None], {"frame": {"duration": 0, "redraw": False}, 
                                     "mode": "immediate"}]}
        self.slider = dict(
            active=0,
            steps=[{
                "method": "animate",
                "label": f"{i}",
                "args": [[f"frame{i}"], {"frame": {"duration": 0, "redraw": True}}]
            } for i in range(0, parent.n, 5)] # data dependance
        )

