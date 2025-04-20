[TOC]

---


# funJplot

[![PyPI version](https://badge.fury.io/py/funJplot.svg)](https://pypi.org/project/funJplot/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub Stars](https://img.shields.io/github/stars/pellacaniSimone/funJplot?style=social)

**funJplot** is a lightweight and simple Python library, specifically designed for creating animations in Jupyter notebooks using NumPy arrays. The main goal is to provide an intuitive tool for learning and visualizing concepts related to mathematical algebra, statistics, and related disciplines.

**Warning: Pre-Alpha Stage**

This library is currently in the pre-alpha phase. This means that the API may undergo significant changes without notice, and there might be bugs or incomplete features. Use in production environments is discouraged. However, we are excited to share our ongoing work and welcome feedback and contributions from the community.

## Key Features (Current)

* Provides abstract base classes (`GeometricAnimation`, `ParametricCurve`) to simplify the creation of geometric animations.
* Includes concrete implementations for common animations:
    * Rotation of a vector (`VectorRotation`) the basc example
    * Archimedean spiral (`Spiral`)
    * Ellipse (`Ellipse`)
    * Lissajous curves (`Lissajous`)
    * Lorenz Attractor (`LorenzAttractor`)
* Integrated user interface with Play/Pause buttons and sliders to control the animation in Jupyter.
* Uses `plotly` for creating interactive graphs and smooth animations.

## Installation

You can install `funJplot` via pip:

```bash
pip install funJplot
```

If you installed from TestPyPI:

```bash
pip install -i [https://test.pypi.org/simple/](https://test.pypi.org/simple/) funJplot
```

Make sure you also have `numpy` and `plotly` installed:

```bash
pip install numpy plotly
```





## How to Use

Here are some basic examples of how to use the provided classes. Make sure to run these commands in a Jupyter notebook to view the interactive animations.

### Example 1: Rotating Vector Animation

```python
from funJplot import VectorRotation

# Create an instance of the vector rotation animation
vector_anim = VectorRotation(frame_count=150, frame_duration_ms=40)

# Show the animation
vector_anim.show()
```

### Example 2: Spiral Animation

```python
from funJplot import Spiral
import numpy as np

# Create an instance of the spiral animation
spiral_anim = Spiral(frame_count=300, frame_duration_ms=25, rotations=5, scale=10, a=0, b=0.4)

# Show the animation
spiral_anim.show()
```

### Example 3: Lorenz Attractor Animation

```python
from funJplot import LorenzAttractor

# Create an instance of the Lorenz attractor animation
lorenz_anim = LorenzAttractor(frame_count=3000, frame_duration_ms=5, scale=40, dt=0.01)

# Show the animation
lorenz_anim.show()
```

## Upcoming Developments (Pre-Alpha Roadmap)

  * Add more geometric animation classes (e.g., linear transformations, waves).
  * Implement basic statistical animations (e.g., evolution of distributions).
  * Improve documentation and provide more examples.
  * Make the API more flexible and configurable.
  * Handle 3D animations.

## Build method

Create a virtual environment

```bash
python3 -m venv .venv
```

Activate the environment

```bash
source .venv/bin/activate
```

Update the environment
```bash
pip install --upgrade pip
```

Add install software
```bash
pip install -r requirement_build.txt
```

Create your `$HOME/.pypirc` file like below or something more customized
```env
[pypi]
  username = __token__
  password = pypi-<Your API key generated from Pypi website>
```

Build your app
```bash
cd src
python3 -m build
```

If you want to test your library, `deactivate` current virtual environment and create a new one into `dist/` folder then, after the activation of test_venv you can:
```bash
VERSION= # version here
cd dist
pip install funjplot-${VERSION}-py3-none-any.whl
```

Now you can push into your pipy:
```bash
python3 -m twine upload  dist/*
```


## Contributions

We are open to contributions and feedback\! If you have ideas, suggestions, or have found bugs, feel free to open an issue on GitHub.

## License

This project is released under the [MIT](https://www.google.com/search?q=LICENSE) license.


##### Thanks to LLM to write some part of code and documentation for this initial version