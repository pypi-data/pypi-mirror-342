from . import vereshchagin_figures as vf

from enum import Enum, auto

def get_figure_pair_type(figure_1, figure_2):

    """
    Determines the type of figure pair based on the two provided figures.

    This function maps combinations of geometric figure classes to a unique
    FigureType enum value. It validates that both figures share the same width (x),
    and returns an appropriate enum constant based on the types of the inputs.

    Args:
        figure_1: The first figure instance.
        figure_2: The second figure instance.

    Returns:
        A FigureType enum member representing the combination of the two figures.

    Raises:
        ValueError: If the figures have mismatched widths (x),
                    or if their type combination is not supported.
    """
    vf.validate_figure(figure_1)
    vf.validate_figure(figure_2)

    if figure_1.x != figure_2.x:
        raise ValueError(f"x of figures doesn't match: x1 = {figure_1.x}, x2 = {figure_2.x}")

    type_1 = type(figure_1)
    type_2 = type(figure_2)
    pair = frozenset([type_1, type_2])

    mapping = {
        frozenset([vf.Rectangle]): FigureType.RECTANGLE_RECTANGLE,
        frozenset([vf.Rectangle, vf.TriangleLeft]): FigureType.RECTANGLE_TRIANGLE_LEFT,
        frozenset([vf.Rectangle, vf.TriangleRight]): FigureType.RECTANGLE_TRIANGLE_RIGHT,
        frozenset([vf.Rectangle, vf.Trapezoid]): FigureType.RECTANGLE_TRAPEZOID,
        frozenset([vf.Rectangle, vf.Parabola]): FigureType.RECTANGLE_PARABOLA,
        frozenset([vf.TriangleLeft]): FigureType.TRIANGLE_LEFT_TRIANGLE_LEFT,
        frozenset([vf.TriangleLeft, vf.TriangleRight]): FigureType.TRIANGLE_LEFT_TRIANGLE_RIGHT,
        frozenset([vf.TriangleLeft, vf.Trapezoid]): FigureType.TRIANGLE_LEFT_TRAPEZOID,
        frozenset([vf.TriangleLeft, vf.Parabola]): FigureType.TRIANGLE_LEFT_PARABOLA,
        frozenset([vf.TriangleRight]): FigureType.TRIANGLE_RIGHT_TRIANGLE_RIGHT,
        frozenset([vf.TriangleRight, vf.Trapezoid]): FigureType.TRIANGLE_RIGHT_TRAPEZOID,
        frozenset([vf.TriangleRight, vf.Parabola]): FigureType.TRIANGLE_RIGHT_PARABOLA,
        frozenset([vf.Trapezoid]): FigureType.TRAPEZOID_TRAPEZOID,
        frozenset([vf.Trapezoid, vf.Parabola]): FigureType.TRAPEZOID_PARABOLA,
        frozenset([vf.Parabola]): FigureType.PARABOLA_PARABOLA,
        frozenset([vf.ParabolicTrapezoid, vf.Rectangle]): FigureType.PARABOLIC_TRAPEZOID_RECTANGLE,
        frozenset([vf.ParabolicTrapezoid, vf.TriangleLeft]): FigureType.PARABOLIC_TRAPEZOID_TRIANGLE_LEFT,
        frozenset([vf.ParabolicTrapezoid, vf.TriangleRight]): FigureType.PARABOLIC_TRAPEZOID_TRIANGLE_RIGHT,
        frozenset([vf.ParabolicTrapezoid, vf.Trapezoid]): FigureType.PARABOLIC_TRAPEZOID_TRAPEZOID,
        frozenset([vf.ParabolicTrapezoid, vf.Parabola]): FigureType.PARABOLIC_TRAPEZOID_PARABOLA,
        frozenset([vf.ParabolicTrapezoid]): FigureType.PARABOLIC_TRAPEZOID_PARABOLIC_TRAPEZOID,
    }
    if pair not in mapping:
        raise ValueError(f"Unsupported figure pair: {pair}")
    return mapping[pair]


class FigureType(Enum):

    """
    Enum representing all supported combinations of figure types.

    Each enum member corresponds to a specific pairing of geometric figures
    (e.g., Rectangle + TriangleLeft, Parabola + Parabola, etc.) and is used
    to drive the correct visualization and integration logic in the system.
    """

    RECTANGLE_RECTANGLE = auto()
    RECTANGLE_TRIANGLE_LEFT = auto()
    RECTANGLE_TRIANGLE_RIGHT = auto()
    RECTANGLE_TRAPEZOID = auto()
    RECTANGLE_PARABOLA = auto()
    TRIANGLE_LEFT_TRIANGLE_LEFT = auto()
    TRIANGLE_LEFT_TRIANGLE_RIGHT = auto()
    TRIANGLE_LEFT_TRAPEZOID = auto()
    TRIANGLE_LEFT_PARABOLA = auto()
    TRIANGLE_RIGHT_TRIANGLE_RIGHT = auto()
    TRIANGLE_RIGHT_TRAPEZOID = auto()
    TRIANGLE_RIGHT_PARABOLA = auto()
    TRAPEZOID_TRAPEZOID = auto()
    TRAPEZOID_PARABOLA = auto()
    PARABOLA_PARABOLA = auto()
    PARABOLIC_TRAPEZOID_RECTANGLE = auto()
    PARABOLIC_TRAPEZOID_TRIANGLE_LEFT = auto()
    PARABOLIC_TRAPEZOID_TRIANGLE_RIGHT = auto()
    PARABOLIC_TRAPEZOID_TRAPEZOID = auto()
    PARABOLIC_TRAPEZOID_PARABOLA = auto()
    PARABOLIC_TRAPEZOID_PARABOLIC_TRAPEZOID = auto()

