# VereshchaginPy

**VereshchaginPy** is a Python library for performing graph multiplication — particularly useful in structural mechanics when applying the flexibility method.

The integration is based on the principle that the integral from two graphs can be expressed as:

```
∫ Mi(x) * Mj(x) dx = A * y
```

Where:
- `A` is the area under the first moment diagram `Mi(x)`
- `y` is the corresponding ordinate (value) from the second moment diagram `Mj(x)` evaluated at the centroid of area `A`
- `Mi`, `Mj` are continuous functions (e.g., moments) over a shared length `L`

This library helps formalize that process by abstracting common shape-based moment diagrams (rectangles, triangles, trapezoids, parabolas) and automating their integration and visualization.

---

## Installation

Install the package via pip:

```bash
pip install vereshchaginpy
```

---

## Example Usage

```python
from vereshchaginpy import Rectangle, TriangleLeft, VereshchaginVisualiser

# Define two figures
r = Rectangle(5, 3)
t = TriangleLeft(5, 2)

# Visualize the interaction
viz = VereshchaginVisualiser()
viz.draw_situation(r, t)

# Compute the integral using the + operator
result = r + t

print(f"Result: {result}")
```

---

## Features

- Support for standard structural figure types:
  - `Rectangle`
  - `TriangleLeft`, `TriangleRight`
  - `Trapezoid`
  - `Parabola`
  - `ParabolicTrapezoid` (combining a parabola and trapezoid)
- Clean and extendable figure model
- Visualizer to plot and label diagrams
- Operator overloading for quick integration via `+`
- Strict input validation for type safety

---

## Project Links

- GitHub: https://github.com/Haudkozaur/VereshchaginPy
- PyPI: https://pypi.org/project/vereshchaginpy

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
