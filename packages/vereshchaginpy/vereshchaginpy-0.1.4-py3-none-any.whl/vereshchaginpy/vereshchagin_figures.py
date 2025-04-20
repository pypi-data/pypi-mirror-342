from abc import ABC, abstractmethod
from .vereshchagin_core import integrate_pair




class Figure(ABC):

    """
    Abstract base class for all Vereshchagin figure types.

    All geometric shapes (e.g., Rectangle, TriangleLeft, Trapezoid) must inherit from this class
    and implement the `__add__` method, which defines how figures can be combined
    into pairs for integration purposes.
    """

    @abstractmethod
    def __add__(self, other):
        """
        Performs integration between two figure instances using the `+` operator.

        This method defines how two compatible Vereshchagin figures interact when added together,
        and returns the result of their integration as a float.

        Args:
            other: Another figure instance to integrate with.

        Returns:
            A float representing the result of the integration between the two figures.
        """
        pass

class Rectangle(Figure):
    """
    Represents a rectangular segment of a linear constant function,
    typically used for plotting or modeling constant-value beam segments.

    Args:
        x (float): The length of the segment (e.g., beam length on the x-axis).
        height (float): The constant value (e.g., force or moment) over the entire segment.
    """

    def __init__(self, x, height):
        self.x = x
        self.height = height

    def __add__(self, other):
        return integrate_pair(self, other)


class TriangleLeft(Figure):
    """
    Represents a left-aligned triangular segment of a linear function,
    where the value linearly increases from 0 to a maximum at the left end.

    Args:
        x (float): The length of the segment (e.g., beam length on the x-axis).
        height (float): The maximum value at the left end of the segment.
    """

    def __init__(self, x, height):
        self.x = x
        self.height = height

    def __add__(self, other):
        return integrate_pair(self, other)


class TriangleRight(Figure):
    """
    Represents a right-aligned triangular segment of a linear function,
    where the value linearly decreases from a maximum at the right end to 0.

    Args:
        x (float): The length of the segment (e.g., beam length on the x-axis).
        height (float): The maximum value at the right end of the segment.
    """
    def __init__(self, x, height):
        self.x = x
        self.height = height

    def __add__(self, other):
        return integrate_pair(self, other)


class Trapezoid(Figure):
    """
    Represents a trapezoidal segment of a linear function,
    where the value changes linearly from a left value to a right value over the segment's length.

    Args:
        x (float): The length of the segment (e.g., beam length on the x-axis).
        height_left (float): The function value at the left end of the segment.
        height_right (float): The function value at the right end of the segment.
    """

    def __init__(self, x, height_left, height_right):
        self.x = x
        self.height_left = height_left
        self.height_right = height_right

    def __add__(self, other):
        return integrate_pair(self, other)


class Parabola(Figure):
    """
    Represents a parabolic segment caused by a uniformly distributed line load
    over a specified length. The resulting function is quadratic, with zero values
    at both ends and a peak (positive or negative) at the midpoint.

    Args:
        x (float): The length of the segment (e.g., beam length on the x-axis).
        line_load (float): The intensity of the uniformly distributed load causing
            the parabolic shape (positive for upward, negative for downward).
    """

    def __init__(self, x, line_load):
        self.x = x
        self.line_load = line_load

    def __add__(self, other):
        return integrate_pair(self, other)


class ParabolicTrapezoid(Figure):
    """
    Represents a parabolic segment with defined boundary values, caused by a constant
    uniformly distributed load acting along the segment's length.

    This class models a function with a parabolic shape that starts at a given value on the left end
    and ends at another value on the right end (which can differ in sign or be zero). The curvature
    of the parabola is the result of a constant distributed load over the segment's length.
    This shape is flexible enough to represent a wide range of complex diagram types,
    especially those that combine linear transitions with curvature induced by loading.

    Args:
        x (float): The length of the segment (e.g., beam length on the x-axis).
        height_left (float): The function value at the left end of the segment.
        height_right (float): The function value at the right end of the segment.
        line_load (float): The intensity of the constant distributed load that
            causes the parabolic curvature.
    """

    def __init__(self, x, height_left, height_right, line_load):
        self.x = x
        self.height_left = height_left
        self.height_right = height_right
        self.line_load = line_load

    def __add__(self, other):
        return integrate_pair(self, other)

def validate_figure(obj):
    """
    Validates that the object is an instance of a supported Vereshchagin figure.

    Args:
        obj: Any object.

    Raises:
        TypeError: If the object is not a supported figure type.
    """
    if not isinstance(obj, (
        Rectangle,
        TriangleLeft,
        TriangleRight,
        Trapezoid,
        Parabola,
        ParabolicTrapezoid
    )):
        raise TypeError(f"Unsupported figure type: {type(obj).__name__}")
