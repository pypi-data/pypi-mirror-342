import vereshchagin_figures as vf
from vereshchagin_pairs import get_figure_pair_type, FigureType

def integrate_pair(figure_1, figure_2):

    """
    Computes the definite integral representing the interaction between two figures.

    Based on the specific combination of figure types, the method applies appropriate
    analytical integration formulas to calculate the area or product under the curve,
    typically used in the context of structural mechanics or moment interactions.

    Args:
        figure_1: The first geometric figure object.
        figure_2: The second geometric figure object.

    Returns:
        A float value representing the computed integral.

    Raises:
        TypeError: If the combination of figure types is unsupported.
        ValueError: If the figures have mismatched widths (`x` values).
    """

    pair_type = get_figure_pair_type(figure_1, figure_2)

    match pair_type:

        case FigureType.RECTANGLE_RECTANGLE:
            return figure_1.x * figure_1.height * figure_2.height

        case FigureType.RECTANGLE_TRIANGLE_LEFT:
            rect, tri = (figure_1, figure_2) if isinstance(figure_1, vf.Rectangle) else (figure_2, figure_1)
            return rect.x * rect.height * (tri.height / 2)

        case FigureType.RECTANGLE_TRIANGLE_RIGHT:
            rect, tri = (figure_1, figure_2) if isinstance(figure_1, vf.Rectangle) else (figure_2, figure_1)
            return rect.x * rect.height * (tri.height / 2)

        case FigureType.RECTANGLE_TRAPEZOID:
            rect, trap = (figure_1, figure_2) if isinstance(figure_1, vf.Rectangle) else (figure_2, figure_1)
            return (rect.x / 6) * (
                2 * rect.height * trap.height_left +
                2 * rect.height * trap.height_right +
                rect.height * trap.height_right +
                rect.height * trap.height_left
            )

        case FigureType.RECTANGLE_PARABOLA:
            rect, par = (figure_1, figure_2) if isinstance(figure_1, vf.Rectangle) else (figure_2, figure_1)
            f = par.line_load * (par.x ** 2) / 8
            return (2 / 3) * (rect.x * f * rect.height)

        case FigureType.TRIANGLE_LEFT_TRIANGLE_LEFT:
            return (1 / 3) * figure_1.x * figure_1.height * figure_2.height

        case FigureType.TRIANGLE_LEFT_TRIANGLE_RIGHT:
            tri_left, tri_right = (figure_1, figure_2) if isinstance(figure_1, vf.TriangleLeft) else (figure_2, figure_1)
            return (1 / 6) * tri_left.x * tri_left.height * tri_right.height

        case FigureType.TRIANGLE_LEFT_TRAPEZOID:
            tri, trap = (figure_1, figure_2) if isinstance(figure_1, vf.TriangleLeft) else (figure_2, figure_1)
            return (tri.x / 6) * (2 * tri.height * trap.height_left + trap.height_right * tri.height)

        case FigureType.TRIANGLE_LEFT_PARABOLA:
            tri, par = (figure_1, figure_2) if isinstance(figure_1, vf.TriangleLeft) else (figure_2, figure_1)
            f = par.line_load * (par.x ** 2) / 8
            return (1 / 3) * (tri.x * f * tri.height)

        case FigureType.TRIANGLE_RIGHT_TRIANGLE_RIGHT:
            return (1 / 3) * figure_1.x * figure_1.height * figure_2.height

        case FigureType.TRIANGLE_RIGHT_PARABOLA:
            tri, par = (figure_1, figure_2) if isinstance(figure_1, vf.TriangleRight) else (figure_2, figure_1)
            f = par.line_load * (par.x ** 2) / 8
            return (1 / 3) * (tri.x * f * tri.height)

        case FigureType.TRIANGLE_RIGHT_TRAPEZOID:
            tri, trap = (figure_1, figure_2) if isinstance(figure_1, vf.TriangleRight) else (figure_2, figure_1)
            return (tri.x / 6) * (2 * tri.height * trap.height_right + trap.height_left * tri.height)

        case FigureType.TRAPEZOID_TRAPEZOID:
            return (figure_1.x / 6) * (
                2 * figure_1.height_left * figure_2.height_left +
                2 * figure_1.height_right * figure_2.height_right +
                figure_1.height_left * figure_2.height_right +
                figure_1.height_right * figure_2.height_left
            )

        case FigureType.PARABOLA_PARABOLA:
            f = figure_1.line_load * (figure_1.x ** 2) / 8
            g = figure_2.line_load * (figure_2.x ** 2) / 8
            return (8 / 15) * (figure_1.x * f * g)

        case FigureType.TRAPEZOID_PARABOLA:
            trap, par = (figure_1, figure_2) if isinstance(figure_1, vf.Trapezoid) else (figure_2, figure_1)
            f = par.line_load * (par.x ** 2) / 8
            triangle_1 = vf.TriangleLeft(trap.x, trap.height_left)
            triangle_2 = vf.TriangleRight(trap.x, trap.height_right)
            return (1 / 3) * (triangle_1.x * f * triangle_1.height + triangle_2.x * f * triangle_2.height)

        case FigureType.PARABOLIC_TRAPEZOID_RECTANGLE:
            parab_trap, rect = (figure_1, figure_2) if isinstance(figure_1, vf.ParabolicTrapezoid) else (figure_2, figure_1)
            parabola = vf.Parabola(parab_trap.x, parab_trap.line_load)
            trapezoid = vf.Trapezoid(parab_trap.x, parab_trap.height_left, parab_trap.height_right)
            return integrate_pair(trapezoid, rect) + integrate_pair(parabola, rect)

        case FigureType.PARABOLIC_TRAPEZOID_TRIANGLE_LEFT:
            parab_trap, tri = (figure_1, figure_2) if isinstance(figure_1, vf.ParabolicTrapezoid) else (figure_2, figure_1)
            parabola = vf.Parabola(parab_trap.x, parab_trap.line_load)
            trapezoid = vf.Trapezoid(parab_trap.x, parab_trap.height_left, parab_trap.height_right)
            return integrate_pair(trapezoid, tri) + integrate_pair(parabola, tri)

        case FigureType.PARABOLIC_TRAPEZOID_TRIANGLE_RIGHT:
            parab_trap, tri = (figure_1, figure_2) if isinstance(figure_1, vf.ParabolicTrapezoid) else (figure_2, figure_1)
            parabola = vf.Parabola(parab_trap.x, parab_trap.line_load)
            trapezoid = vf.Trapezoid(parab_trap.x, parab_trap.height_left, parab_trap.height_right)
            return integrate_pair(trapezoid, tri) + integrate_pair(parabola, tri)

        case FigureType.PARABOLIC_TRAPEZOID_TRAPEZOID:
            parab_trap, trap = (figure_1, figure_2) if isinstance(figure_1, vf.ParabolicTrapezoid) else (figure_2, figure_1)
            parabola = vf.Parabola(parab_trap.x, parab_trap.line_load)
            trapezoid = vf.Trapezoid(parab_trap.x, parab_trap.height_left, parab_trap.height_right)
            return integrate_pair(trapezoid, trap) + integrate_pair(parabola, trap)

        case FigureType.PARABOLIC_TRAPEZOID_PARABOLA:
            parab_trap, par = (figure_1, figure_2) if isinstance(figure_1, vf.ParabolicTrapezoid) else (figure_2, figure_1)
            parabola = vf.Parabola(parab_trap.x, parab_trap.line_load)
            trapezoid = vf.Trapezoid(parab_trap.x, parab_trap.height_left, parab_trap.height_right)
            return integrate_pair(trapezoid, par) + integrate_pair(parabola, par)

        case FigureType.PARABOLIC_TRAPEZOID_PARABOLIC_TRAPEZOID:
            parab_trap_1, parab_trap_2 = figure_1, figure_2
            parabola_1 = vf.Parabola(parab_trap_1.x, parab_trap_1.line_load)
            parabola_2 = vf.Parabola(parab_trap_2.x, parab_trap_2.line_load)
            trapezoid_1 = vf.Trapezoid(parab_trap_1.x, parab_trap_1.height_left, parab_trap_1.height_right)
            trapezoid_2 = vf.Trapezoid(parab_trap_2.x, parab_trap_2.height_left, parab_trap_2.height_right)
            return (
                integrate_pair(parabola_1, parabola_2) +
                integrate_pair(trapezoid_1, trapezoid_2) +
                integrate_pair(parabola_1, trapezoid_2) +
                integrate_pair(parabola_2, trapezoid_1)
            )

        case _:
            raise TypeError(f"Unsupported figure combination: {type(figure_1).__name__} + {type(figure_2).__name__}")
