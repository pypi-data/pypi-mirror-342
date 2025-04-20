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
                "buttons": [self.gui.play, self.gui.pause],
                "x": 0.1, "y": 0, "xanchor": "left", "yanchor": "bottom"
            }],
            sliders=[self.gui.slider]
        )
        return initial_figure 
    


class MathMul(GeometricAnimation):
    """2d example of matrix and vector multiplication

    Args:
        A (np.array): 2x2 Matrix left
        B (np.array): 2x2 Matrix right
        v (np.array): 2x1 vector

        frame_count (int, optional): n animation frames Defaults to 100.
        duration (int, optional): seconds time Defaults to 50.
        scale (float, optional): image reference scaling Defaults to 1.5.
        
    """
    def __init__(self, A, B, v, frame_count=100, duration=50, scale=1.5):

        super().__init__(frame_count, duration, scale)
        self.A = A
        self.B = B
        self.C = A @ B
        self.v = v
        self.gui = GuiInterface(self)

        # interpolations v e Av, Bv, Cv
        self.vA = self.A @ self.v
        self.vB = self.B @ self.v
        self.vC = self.C @ self.v

        self.steps_A = np.linspace(self.v, self.vA, self.n)
        self.steps_B = np.linspace(self.v, self.vB, self.n)
        self.steps_C = np.linspace(self.v, self.vC, self.n)

    def _make_trace(self, vec, color, name):
        return go.Scatter(x=[0, vec[0]], y=[0, vec[1]],
                          mode='lines+markers',
                          line=dict(width=3, color=color),
                          marker=dict(size=6),
                          name=name)

    def _create_figure(self):
        fig = go.Figure(
            data=[
                self._make_trace(self.v, 'red', 'v'),
                self._make_trace(self.steps_A[0], 'blue', 'A·v'),
                self._make_trace(self.steps_B[0], 'green', 'B·v'),
                self._make_trace(self.steps_C[0], 'purple', '(A·B)·v'),
            ]
        )

        fig.frames = [
            go.Frame(
                data=[
                    self._make_trace(self.v, 'red', 'v'),
                    self._make_trace(self.steps_A[i], 'blue', 'A·v'),
                    self._make_trace(self.steps_B[i], 'green', 'B·v'),
                    self._make_trace(self.steps_C[i], 'purple', '(A·B)·v')
                ],
                name=f"frame{i}"
            )
            for i in range(self.n)
        ]

        fig.update_layout(
            title="Matrix multiplication animation on a 2D vector",
            xaxis=dict(title="X", range=[-self.scale, self.scale], constrain='domain'),
            yaxis=dict(title="Y", range=[-self.scale, self.scale], scaleanchor="x", scaleratio=1),
            width=700,
            height=700,
            updatemenus=[{
                "type": "buttons",
                "buttons": [self.gui.play, self.gui.pause],
                "x": 0.1, "y": 0, "xanchor": "left", "yanchor": "bottom"
            }],
            sliders=[self.gui.slider]
        )

        return fig