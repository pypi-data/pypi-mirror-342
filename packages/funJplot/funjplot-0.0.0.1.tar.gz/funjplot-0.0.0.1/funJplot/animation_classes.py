# Import necessary libraries
import numpy as np
import plotly.graph_objects as go
from abc import ABC, abstractmethod # Used for creating abstract base classes

class GeometricAnimation(ABC):
    """Abstract base class for geometric animations."""

    @abstractmethod
    def __init__(self, frame_count=100, frame_duration_ms=50, plot_scale=1.09):
        """
        Abstract initializer that must be implemented by subclasses.

        Args:
            frame_count (int): The total number of frames in the animation.
            frame_duration_ms (int): The duration of each frame in milliseconds.
            plot_scale (float): A factor to set the initial range of the plot axes.
        """
        # Store animation parameters
        self.frame_count = frame_count
        self.frame_duration_ms = frame_duration_ms
        self.plot_scale = plot_scale


    @abstractmethod
    def _create_figure(self):
        """
        Abstract method to create the Plotly figure for the animation.
        This must be implemented by subclasses.
        """
        pass

    def show(self):
        """Creates the figure using the subclass implementation and displays the animation."""
        figure = self._create_figure()
        if figure:
            figure.show()




class GuiInterface:
    """Class to manage the user interface elements (buttons, slider) for animations."""

    def __init__(self, parent_animation):
        """
        Initializes the GUI elements based on the parent animation's properties.

        Args:
            parent_animation: The animation object (e.g., ParametricCurve, VectorRotation)
                              that this GUI controls.
        """
        self.parent_animation = parent_animation


        # Define the 'Play' button configuration
        self.play_button = {
            "label": "Play",
            "method": "animate",
            "args": [
                None,
                {
                    "frame": {"duration": self.parent_animation.frame_duration_ms, "redraw": True},
                    "fromcurrent": True, # Start animation from the current frame
                    "transition": {"duration": 0} # Avoid smooth transition between frames when playing
                }
            ]
        }


        # Define the 'Pause' button configuration
        self.pause_button = {
            "label": "Pause",
            "method": "animate",
            "args": [
                [None], # Target frame name (None stops animation)
                {
                    "frame": {"duration": 0, "redraw": False}, # Stop immediately, don't redraw
                    "mode": "immediate" # Apply changes immediately
                }
            ]
        }


        # Define the slider configuration
        self.slider_steps = [
            {
                "method": "animate",
                "label": f"{i}", # Label for the slider step (frame number)
                "args": [
                    [f"frame{i}"], # Go to specific frame name
                    {
                        "frame": {"duration": 0, "redraw": True}, # Go immediately, redraw
                        "mode": "immediate"
                    }
                ]
            }
            # Create steps for the slider, typically less dense than total frames for usability
            # Showing a step every 5 frames here.
            for i in range(0, self.parent_animation.frame_count, 5)
        ]
        self.animation_slider = dict(
            active=0, # Default active step
            currentvalue={"prefix": "Frame: "}, # Display prefix for current value
            pad={"t": 50}, # Padding top of slider
            steps=self.slider_steps
        )



class ParametricCurve(GeometricAnimation):
    """Abstract base class for animating 2D parametric curves (x(t), y(t))."""

    @abstractmethod
    def __init__(self, frame_count=100, frame_duration_ms=50, plot_scale=1.09, rotations=4):
        """
        Initializer for parametric curve animations.

        Args:
            frame_count (int): Total animation frames.
            frame_duration_ms (int): Duration per frame (ms).
            plot_scale (float): Scaling factor for plot axes.
            rotations (float): Number of 2*pi cycles for the parameter 't'.
        """

        super().__init__(frame_count, frame_duration_ms, plot_scale)
        self.rotations = rotations
        # Create the GUI interface associated with this animation
        self.gui = GuiInterface(self)
        # Placeholder for coordinates, will be computed later
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

        # Generate the parameter values 't' over the specified number of rotations
        # A full rotation corresponds to 2*pi
        parameter_values = np.linspace(0, self.rotations * 2 * np.pi, self.frame_count)


        # Compute the x and y coordinates using the subclass's implementation
        self.x_coordinates, self.y_coordinates = self.compute_points(parameter_values)


        if self.x_coordinates is None or self.y_coordinates is None:
             return None

        # Create the initial figure object with the first point/segment
        # The animation will build upon this.
        initial_figure = go.Figure(
            data=[go.Scatter(x=self.x_coordinates[:1], y=self.y_coordinates[:1],
                             mode='lines+markers', # Show both lines and markers
                             line=dict(width=2),
                             marker=dict(size=4))]
        )


        # Create the animation frames
        # Each frame adds one more point/segment to the plot
        animation_frames = [
            go.Frame(
                data=[go.Scatter(x=self.x_coordinates[:i+1], y=self.y_coordinates[:i+1],
                                 mode='lines+markers', # Update data for the trace
                                 line=dict(width=2),
                                 marker=dict(size=4))],
                name=f"frame{i}" # Naming frames is important for slider/button control
            )
            for i in range(1, self.frame_count) # Start from frame 1 as frame 0 is the initial figure
        ]
        initial_figure.frames = animation_frames


        # Configure the layout of the figure (titles, axes, buttons, slider)
        initial_figure.update_layout(
            title=f"{self.__class__.__name__} Animation", # Use the subclass name for the title
            xaxis=dict(
                title="X-axis",
                range=[-self.plot_scale, self.plot_scale],
                constrain='domain' # Keep X axis fixed relative to plot size
                ),
            yaxis=dict(
                title="Y-axis",
                range=[-self.plot_scale, self.plot_scale],
                scaleanchor="x", # Make y scale match x scale for aspect ratio 1:1
                scaleratio=1
                ),
            width=700, # Figure width in pixels
            height=700, # Figure height in pixels
            updatemenus=[{
                "type": "buttons",
                "buttons": [self.gui.play_button, self.gui.pause_button],
                "x": 0.1, "y": 0, "xanchor": "left", "yanchor": "bottom" # Position buttons
            }],
            sliders=[self.gui.animation_slider] # Add the slider
        )

        return initial_figure


class VectorRotation(GeometricAnimation):
    """Specific implementation for animating a rotating 2D unit vector."""

    def __init__(self, frame_count=100, frame_duration_ms=50, plot_scale=1.2):
        """
        Initializer for the VectorRotation animation.

        Args:
            frame_count (int): Total animation frames.
            frame_duration_ms (int): Duration per frame (ms).
            plot_scale (float): Scaling factor for plot axes.
        """
        super().__init__(frame_count, frame_duration_ms, plot_scale)
        # Calculate angles for each frame (simple linear progression)
        # The factor 10 determines the speed/total rotation angle
        self.rotation_angles = np.linspace(0, self.frame_count / 10.0, self.frame_count)
        # Pre-calculate cosine and sine values for efficiency
        self.cosine_values = np.cos(self.rotation_angles)
        self.sine_values = np.sin(self.rotation_angles)
        # Create the GUI interface
        self.gui = GuiInterface(self)

    def _create_figure(self):
        """Creates the Plotly figure and frames for the vector rotation animation."""
        # Create the initial figure showing the vector at the first angle
        initial_figure = go.Figure(
            data=[go.Scatter(x=[0, self.cosine_values[0]], y=[0, self.sine_values[0]],
                             mode='lines+markers', # Vector as line from origin
                             line=dict(width=3),
                             marker=dict(size=6))]
        )

        # Create animation frames, each showing the vector at a subsequent angle
        animation_frames = [
            go.Frame(
                data=[go.Scatter(x=[0, self.cosine_values[i]], y=[0, self.sine_values[i]],
                                 mode='lines+markers',
                                 line=dict(width=3),
                                 marker=dict(size=6))],
                name=f"frame{i}" # Name the frame
            )
            for i in range(self.frame_count)
        ]
        initial_figure.frames = animation_frames

        # Configure the layout (title, axes, buttons, slider)
        initial_figure.update_layout(
            title="Vector Rotation Animation",
            xaxis=dict(
                title="X-axis",
                range=[-self.plot_scale, self.plot_scale],
                 constrain='domain'
                ),
            yaxis=dict(
                title="Y-axis",
                range=[-self.plot_scale, self.plot_scale],
                scaleanchor="x",
                scaleratio=1
                ),
            width=600, height=600,
            updatemenus=[{
                "type": "buttons",
                "buttons": [self.gui.play_button, self.gui.pause_button],
                 "x": 0.1, "y": 0, "xanchor": "left", "yanchor": "bottom"
            }],
            sliders=[self.gui.animation_slider]
        )
        return initial_figure

# --- Concrete Implementations of Parametric Curves ---

class Spiral(ParametricCurve):
    """
    Implementation of a parametric Archimedean spiral: r = a + b*theta.
    x = r * cos(theta), y = r * sin(theta)
    """
    def __init__(self, frame_count=200, frame_duration_ms=30, plot_scale=5, rotations=4, a=0.5, b=0.2):
        """
        Initializer for the Spiral animation.

        Args:
            frame_count (int): Total frames.
            frame_duration_ms (int): Duration per frame (ms).
            plot_scale (float): Axes scaling.
            rotations (float): Number of 2*pi cycles for theta.
            a (float): Starting radius offset.
            b (float): Growth factor of the spiral radius per radian.
        """
        # Store spiral specific parameters
        self.a_param = a
        self.b_param = b
        # Call the parent class initializer
        super().__init__(frame_count, frame_duration_ms, plot_scale, rotations)

    def compute_points(self, t_parameter):
        """
        Computes the (x, y) points for the spiral.

        Args:
            t_parameter (np.array): Array of angle values (theta).

        Returns:
            tuple: (x_coordinates, y_coordinates) as np.arrays.
        """
        # Calculate radius 'r' based on the angle 't' (theta)
        radius = self.a_param + self.b_param * t_parameter
        # Convert polar coordinates (r, t) to Cartesian coordinates (x, y)
        x = radius * np.cos(t_parameter)
        y = radius * np.sin(t_parameter)
        return x, y


class Ellipse(ParametricCurve):
    """
    Implementation of a parametric ellipse:
    x = a * cos(t), y = b * sin(t)
    """
    def __init__(self, frame_count=200, frame_duration_ms=30, plot_scale=3, rotations=1, a=2, b=1):
        """
        Initializer for the Ellipse animation.

        Args:
            frame_count (int): Total frames.
            frame_duration_ms (int): Duration per frame (ms).
            plot_scale (float): Axes scaling.
            rotations (float): Number of 2*pi cycles for parameter 't'. (1 rotation completes the ellipse).
            a (float): Semi-major axis (along x-axis).
            b (float): Semi-minor axis (along y-axis).
        """
        # Store ellipse specific parameters
        self.semi_major_axis = a
        self.semi_minor_axis = b
        # Call the parent class initializer
        # Note: `rotations` > 1 will trace the ellipse multiple times.
        super().__init__(frame_count, frame_duration_ms, plot_scale, rotations)

    def compute_points(self, t_parameter):
        """
        Computes the (x, y) points for the ellipse.

        Args:
            t_parameter (np.array): Array of parameter values 't'.

        Returns:
            tuple: (x_coordinates, y_coordinates) as np.arrays.
        """
        # Calculate x and y coordinates using the standard parametric equations for an ellipse
        x = self.semi_major_axis * np.cos(t_parameter)
        y = self.semi_minor_axis * np.sin(t_parameter)
        return x, y


class Lissajous(ParametricCurve):
    """
    Implementation of a Lissajous curve:
    x = a * sin(n * t + delta), y = b * sin(m * t)
    """
    def __init__(self, frame_count=300, frame_duration_ms=20, plot_scale=1.5, rotations=4,
                 a=1, b=1, phase_delta=np.pi/2, freq_n=3, freq_m=2):
        """
        Initializer for the Lissajous curve animation.

        Args:
            frame_count (int): Total frames.
            frame_duration_ms (int): Duration per frame (ms).
            plot_scale (float): Axes scaling.
            rotations (float): Number of 2*pi cycles for parameter 't'.
            a (float): Amplitude of the x-component oscillation.
            b (float): Amplitude of the y-component oscillation.
            phase_delta (float): Phase difference between the oscillations (in radians).
            freq_n (float): Frequency factor for the x-component.
            freq_m (float): Frequency factor for the y-component.
        """
        # Store Lissajous specific parameters
        self.amplitude_a = a
        self.amplitude_b = b
        self.phase_delta = phase_delta
        self.frequency_n = freq_n # Typically related to x-frequency
        self.frequency_m = freq_m # Typically related to y-frequency
        # Call the parent class initializer
        # Important: Need frame_count and rotations carefully chosen depending on n,m to close the curve if desired.
        # We pass the original 'n' (frame_count) to the parent here.
        super().__init__(frame_count, frame_duration_ms, plot_scale, rotations)
        # Note: The original Lissajous class had self.n and self.m as parameters,
        # while the base class uses self.n for frame_count. Renamed here to avoid conflict.
        # The parent class's self.frame_count is what determines the number of points/frames.

    def compute_points(self, t_parameter):
        """
        Computes the (x, y) points for the Lissajous curve.

        Args:
            t_parameter (np.array): Array of parameter values 't'.

        Returns:
            tuple: (x_coordinates, y_coordinates) as np.arrays.
        """
        # Calculate x and y coordinates using Lissajous equations
        x = self.amplitude_a * np.sin(self.frequency_n * t_parameter + self.phase_delta)
        y = self.amplitude_b * np.sin(self.frequency_m * t_parameter)
        return x, y


class LorenzAttractor(ParametricCurve):
    """
    Implementation of the Lorenz attractor (projected onto the X-Y plane).
    Uses the Euler method to solve the Lorenz system of differential equations:
    dx/dt = sigma * (y - x)
    dy/dt = x * (rho - z) - y
    dz/dt = x * y - beta * z
    """
    def __init__(self, frame_count=1500, frame_duration_ms=10, plot_scale=30,
                 # rotations parameter is not directly used here, time evolution depends on dt and frame_count
                 sigma=10.0, rho=28.0, beta=8.0/3.0, dt=0.01, initial_pos=(1.0, 1.0, 1.0)):
        """
        Initializer for the Lorenz Attractor animation.

        Args:
            frame_count (int): Total points/frames to compute.
            frame_duration_ms (int): Duration per frame (ms).
            plot_scale (float): Axes scaling for the X-Y plot.
            sigma (float): Prandtl number parameter.
            rho (float): Rayleigh number parameter.
            beta (float): Geometric parameter.
            dt (float): Time step for the Euler integration method.
            initial_pos (tuple): Initial (x, y, z) position.
        """
        # Store Lorenz system parameters
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.time_step = dt
        self.initial_x, self.initial_y, self.initial_z = initial_pos
        # Note: The 'rotations' parameter from ParametricCurve isn't directly applicable here.
        # The evolution length depends on frame_count * dt. We pass a dummy value (e.g., 1)
        # to the parent constructor, but it's not used by compute_points.
        super().__init__(frame_count, frame_duration_ms, plot_scale, rotations=1)


    def compute_points(self, t_parameter):
        """
        Computes the (x, y) points for the Lorenz attractor projection using Euler method.
        The input 't_parameter' is ignored here; the number of steps is determined
        by self.frame_count set during initialization.

        Args:
            t_parameter (np.array): Ignored in this implementation.

        Returns:
            tuple: (x_coordinates, y_coordinates) as np.arrays representing the X-Y projection.
        """
        num_steps = self.frame_count # Use frame_count as the number of integration steps

        # Initialize arrays to store the coordinates
        x_coords = np.zeros(num_steps)
        y_coords = np.zeros(num_steps)
        z_coords = np.zeros(num_steps) # Although we only plot x,y, we need z for calculation

        # Set initial conditions
        x_coords[0], y_coords[0], z_coords[0] = self.initial_x, self.initial_y, self.initial_z

        # Solve the Lorenz equations step-by-step using the Euler method
        for i in range(num_steps - 1):
            # Calculate the changes (derivatives * dt)
            delta_x = self.sigma * (y_coords[i] - x_coords[i]) * self.time_step
            delta_y = (x_coords[i] * (self.rho - z_coords[i]) - y_coords[i]) * self.time_step
            delta_z = (x_coords[i] * y_coords[i] - self.beta * z_coords[i]) * self.time_step

            # Update the coordinates for the next step
            x_coords[i+1] = x_coords[i] + delta_x
            y_coords[i+1] = y_coords[i] + delta_y
            z_coords[i+1] = z_coords[i] + delta_z

        # This class inherits from ParametricCurve which expects 2D (x, y) data.
        # We return only the x and y coordinates for compatibility with the base class plotting.
        return x_coords, y_coords


# --- Example Usage ---
if __name__ == "__main__":
    print("\n--- Running Vector Rotation Example ---")
    vector_anim = VectorRotation(frame_count=150, duration=40)
    # vector_anim.show() # Uncomment to display

    print("\n--- Running Spiral Example ---")
    spiral_anim = Spiral(frame_count=300, frame_duration_ms=25, rotations=5, plot_scale=10, a=0, b=0.4)
    # spiral_anim.show() # Uncomment to display

    print("\n--- Running Ellipse Example ---")
    ellipse_anim = Ellipse(frame_count=100, frame_duration_ms=40, rotations=2, a=3, b=1.5, plot_scale=3.5)
    # ellipse_anim.show() # Uncomment to display

    print("\n--- Running Lissajous Example ---")
    # Try changing freq_n, freq_m, phase_delta for different patterns
    lissajous_anim = Lissajous(frame_count=400, frame_duration_ms=20, rotations=1, # 1 rotation often enough if n,m are integers
                              plot_scale=1.2, a=1, b=1, freq_n=5, freq_m=4, phase_delta=np.pi/4)
    # lissajous_anim.show() # Uncomment to display

    print("\n--- Running Lorenz Attractor Example ---")
    lorenz_anim = LorenzAttractor(frame_count=3000, frame_duration_ms=5, plot_scale=40, dt=0.01)
    lorenz_anim.show() # Display the last one by default

    print("\n--- Example Usage Finished ---")
