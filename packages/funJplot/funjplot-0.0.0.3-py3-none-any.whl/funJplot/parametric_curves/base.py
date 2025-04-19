from ..base import GeometricAnimation, GuiInterface
import numpy as np
import plotly.graph_objects as go
from abc import abstractmethod

class ParametricCurve(GeometricAnimation):
    """Abstract base class for animating 2D parametric curves (x(t), y(t))."""

    @abstractmethod
    def __init__(self, frame_count=100, frame_duration_ms=50, scale=1.09, rotations=4):
        """
        Initializer for parametric curve animations.

        Args:
            frame_count (int): Total animation frames.
            frame_duration_ms (int): Duration per frame (ms).
            scale (float): Scaling factor for plot axes.
            rotations (float): Number of 2*pi cycles for the parameter 't'.
        """
        super().__init__(frame_count, frame_duration_ms, scale)
        self.rotations = rotations
        self.gui = GuiInterface(self)
        self.x_coordinates = None
        self.y_coordinates = None

    @abstractmethod
    def compute_points(self, t_parameter):
        """
        Abstract method to compute the (x, y) coordinates of the curve
        for a given array of parameter values 't'. Must be implemented by subclasses.

        Args:
            t_parameter (np.array): Array of parameter values.

        Returns:
            tuple: A tuple containing two np.arrays (x_coordinates, y_coordinates).
        """
        pass

    def _create_figure(self):
        """Creates the Plotly figure and frames for the parametric curve animation."""
        parameter_values = np.linspace(0, self.rotations * 2 * np.pi, self.n)
        self.x_coordinates, self.y_coordinates = self.compute_points(parameter_values)

        if self.x_coordinates is None or self.y_coordinates is None:
            return None

        initial_figure = go.Figure(
            data=[go.Scatter(x=self.x_coordinates[:1], y=self.y_coordinates[:1],
                           mode='lines+markers',
                           line=dict(width=2),
                           marker=dict(size=4))]
        )

        animation_frames = [
            go.Frame(
                data=[go.Scatter(x=self.x_coordinates[:i+1], y=self.y_coordinates[:i+1],
                               mode='lines+markers',
                               line=dict(width=2),
                               marker=dict(size=4))],
                name=f"frame{i}"
            )
            for i in range(1, self.n)
        ]
        initial_figure.frames = animation_frames

        initial_figure.update_layout(
            title=f"{self.__class__.__name__} Animation",
            xaxis=dict(
                title="X-axis",
                range=[-self.scale, self.scale],
                constrain='domain'
            ),
            yaxis=dict(
                title="Y-axis",
                range=[-self.scale, self.scale],
                scaleanchor="x",
                scaleratio=1
            ),
            width=700,
            height=700,
            updatemenus=[{
                "type": "buttons",
                "buttons": [self.gui.play_button, self.gui.pause_button],
                "x": 0.1, "y": 0, "xanchor": "left", "yanchor": "bottom"
            }],
            sliders=[self.gui.animation_slider]
        )

        return initial_figure 