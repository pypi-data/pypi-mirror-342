from ..base import GeometricAnimation, GuiInterface
import numpy as np
import plotly.graph_objects as go

class VectorRotation(GeometricAnimation):
    """Specific implementation for animating a rotating 2D unit vector."""

    def __init__(self, frame_count:int=100, frame_duration_ms:int=50, scale:float=1.2):
        """Initializer for the VectorRotation animation."""
        super().__init__(frame_count, frame_duration_ms, scale) 
        self.rotation_angles = np.linspace(0, self.n / 10.0, self.n)
        self.cosine_values = np.cos(self.rotation_angles)
        self.sine_values = np.sin(self.rotation_angles)
        self.gui = GuiInterface(self)

    def _create_figure(self):
        """Creates the Plotly figure and frames for the vector rotation animation."""
        initial_figure = go.Figure(
            data=[go.Scatter(x=[0, self.cosine_values[0]], y=[0, self.sine_values[0]],
                           mode='lines+markers',
                           line=dict(width=3),
                           marker=dict(size=6))]
        )

        animation_frames = [
            go.Frame(
                data=[go.Scatter(x=[0, self.cosine_values[i]], y=[0, self.sine_values[i]],
                               mode='lines+markers',
                               line=dict(width=3),
                               marker=dict(size=6))],
                name=f"frame{i}"
            )
            for i in range(self.n)
        ]
        initial_figure.frames = animation_frames

        initial_figure.update_layout(
            title="Vector Rotation Animation",
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
            width=600,
            height=600,
            updatemenus=[{
                "type": "buttons",
                "buttons": [self.gui.play_button, self.gui.pause_button],
                "x": 0.1, "y": 0, "xanchor": "left", "yanchor": "bottom"
            }],
            sliders=[self.gui.animation_slider]
        )
        return initial_figure 
    


    