import numpy as np
from .base import ParametricCurve

class Spiral(ParametricCurve):
    """Implementation of a parametric Archimedean spiral."""
    
    def __init__(self, frame_count=200, frame_duration_ms=30, plot_scale=5, rotations=4, a=0.5, b=0.2):
        self.a_param = a
        self.b_param = b
        super().__init__(frame_count, frame_duration_ms, plot_scale, rotations)

    def compute_points(self, t_parameter):
        radius = self.a_param + self.b_param * t_parameter
        x = radius * np.cos(t_parameter)
        y = radius * np.sin(t_parameter)
        return x, y


class Ellipse(ParametricCurve):
    """Implementation of a parametric ellipse."""
    
    def __init__(self, frame_count=200, frame_duration_ms=30, plot_scale=3, rotations=1, a=2, b=1):
        self.semi_major_axis = a
        self.semi_minor_axis = b
        super().__init__(frame_count, frame_duration_ms, plot_scale, rotations)

    def compute_points(self, t_parameter):
        x = self.semi_major_axis * np.cos(t_parameter)
        y = self.semi_minor_axis * np.sin(t_parameter)
        return x, y


class Lissajous(ParametricCurve):
    """Implementation of a Lissajous curve."""
    
    def __init__(self, frame_count=300, frame_duration_ms=20, plot_scale=1.5, rotations=4,
                 a=1, b=1, phase_delta=np.pi/2, freq_n=3, freq_m=2):
        self.amplitude_a = a
        self.amplitude_b = b
        self.phase_delta = phase_delta
        self.frequency_n = freq_n
        self.frequency_m = freq_m
        super().__init__(frame_count, frame_duration_ms, plot_scale, rotations)

    def compute_points(self, t_parameter):
        x = self.amplitude_a * np.sin(self.frequency_n * t_parameter + self.phase_delta)
        y = self.amplitude_b * np.sin(self.frequency_m * t_parameter)
        return x, y


class LorenzAttractor(ParametricCurve):
    """Implementation of the Lorenz attractor (projected onto the X-Y plane)."""
    
    def __init__(self, frame_count=1500, frame_duration_ms=10, plot_scale=30,
                 sigma=10.0, rho=28.0, beta=8.0/3.0, dt=0.01, initial_pos=(1.0, 1.0, 1.0)):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.time_step = dt
        self.initial_x, self.initial_y, self.initial_z = initial_pos
        super().__init__(frame_count, frame_duration_ms, plot_scale, rotations=1)

    def compute_points(self, t_parameter):
        num_steps = self.n
        x_coords = np.zeros(num_steps)
        y_coords = np.zeros(num_steps)
        z_coords = np.zeros(num_steps)

        x_coords[0], y_coords[0], z_coords[0] = self.initial_x, self.initial_y, self.initial_z

        for i in range(num_steps - 1):
            delta_x = self.sigma * (y_coords[i] - x_coords[i]) * self.time_step
            delta_y = (x_coords[i] * (self.rho - z_coords[i]) - y_coords[i]) * self.time_step
            delta_z = (x_coords[i] * y_coords[i] - self.beta * z_coords[i]) * self.time_step

            x_coords[i+1] = x_coords[i] + delta_x
            y_coords[i+1] = y_coords[i] + delta_y
            z_coords[i+1] = z_coords[i] + delta_z

        return x_coords, y_coords
    
