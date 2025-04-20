import numpy as np
from ..base import GeometricAnimation, GuiInterface
import plotly.graph_objects as go

class LorenzAttractor3D(GeometricAnimation):
    """Implementation of the Lorenz attractor 3D"""
    
    def __init__(self, frame_count=2000, duration=20, scale=40, 
                 sigma=10, rho=28, beta=8/3, dt=0.01):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.dt = dt
        super().__init__(frame_count, duration, scale)
        self.gui = GuiInterface(self)
    
    def _create_figure(self):
        # Solver Lorenz equations
        n = self.n
        x, y, z = np.zeros(n), np.zeros(n), np.zeros(n)
        x[0], y[0], z[0] = 1.0, 1.0, 1.0
        
        for i in range(n-1):
            dx = self.sigma * (y[i] - x[i]) * self.dt
            dy = (x[i] * (self.rho - z[i]) - y[i]) * self.dt
            dz = (x[i] * y[i] - self.beta * z[i]) * self.dt
            
            x[i+1] = x[i] + dx
            y[i+1] = y[i] + dy
            z[i+1] = z[i] + dz
        

        fig = go.Figure(
            data=[go.Scatter3d(
                x=x[:1], y=y[:1], z=z[:1],
                mode='lines',
                line=dict(width=2, color='blue')
            )]  
        )
        

        fig.frames = [
            go.Frame(
                data=[go.Scatter3d(
                    x=x[:i+1], y=y[:i+1], z=z[:i+1],
                    mode='lines',
                    line=dict(width=2, color='blue'))
                ],
                name=f"frame{i}"
            ) for i in range(1, n)
        ]
        

        fig.update_layout(
            title="Lorenz 3D",
            scene=dict(
                xaxis=dict(title='X', range=[-self.scale, self.scale]),
                yaxis=dict(title='Y', range=[-self.scale, self.scale]),
                zaxis=dict(title='Z', range=[0, self.scale]),
                aspectratio=dict(x=1, y=1, z=0.7)
            ),
            width=800, height=600,
            updatemenus=[{"type": "buttons", "buttons": [self.gui.play, self.gui.pause]}],
            sliders=[self.gui.slider]
        )
        
        return fig