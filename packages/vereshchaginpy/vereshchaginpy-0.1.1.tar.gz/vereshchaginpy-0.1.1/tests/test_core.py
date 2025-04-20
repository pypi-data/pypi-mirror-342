import pytest
import vereshchagin_figures as vf
from vereshchagin_visualise import VereshchaginVisualiser

@pytest.mark.parametrize(
    "fig1, fig2, expected",
    [
        ### Basic cases:
        (vf.Rectangle(5, 3), vf.Rectangle(5, 4), 5*3*4),
        (vf.Rectangle(4, -2), vf.Rectangle(4, 7), 4*(-2)*7),

        (vf.Rectangle(1, 2), vf.TriangleLeft(1, -4), 1*2*(-4)/2),
        (vf.TriangleLeft(6, 19), vf.Rectangle(6, 18), 6*18*19/2),

        (vf.Rectangle(9, 2), vf.TriangleRight(9, 4), 9*2*4/2),
        (vf.TriangleRight(9, -0.5),vf.Rectangle(9, -8), 9*(-8)*(-0.5)/2),

        (vf.Rectangle(5, 5), vf.Trapezoid(5, 1, 0.62), (5/6) * (2*5*1 + 2*5*0.62 + 5*0.62 + 5*1)),
        (vf.Trapezoid(5, -10, 0.7), vf.Rectangle(5, -3), (5/6) * (2*(-10)*(-3) + 2*0.7*(-3) + (-3)*0.7 + (-3)*(-10))),

        (vf.Rectangle(7.5, -2), vf.Parabola(7.5, 25), -1757.8125),

        (vf.TriangleLeft(2.5, -17.24), vf.TriangleLeft(2.5, 11), (1/3)*2.5*(-17.24)*11),
        (vf.TriangleLeft(13, 2.25), vf.TriangleRight(13, 7.6), (1/6) * 13*2.25*7.6),
        (vf.TriangleRight(2.5, -11), vf.TriangleLeft(2.5, 333.33), (1/6)*2.5*(-11)*333.33),
        (vf.TriangleLeft(10, 5), vf.Trapezoid(10, 4, 5), (10/6)*(2*5*4 + 5*5)),
        (vf.TriangleLeft(2, 4.5), vf.Parabola(2, 4), (1/3)*2*4.5*(4*2**2/8)),

        (vf.TriangleRight(6, 7), vf.TriangleRight(6, 5), (1/3)*6*7*5),
        (vf.TriangleRight(4, 2), vf.Trapezoid(4, 5, -6), (4/6)* (2*(-6)*2 + 2*5)),
        (vf.TriangleRight(1, 6), vf.Parabola(1, -5), (1/3)*1*((-5*1**2)/8)*6),

        (vf.Trapezoid(1, 2, 3), vf.Trapezoid(1, 5, 6), (1/6) * (2*3*6 + 2*2*5 + 2*6 + 5*3)),
        (vf.Trapezoid(10, -2, 3), vf.Parabola(10, -5), (1/3) * (10*3*((-5*10**2)/8)) + (1/3) * (10*(-2)*((-5*10**2)/8))),

        (vf.Parabola(5.5, 2), vf.Parabola(5.5, -4.77), (8/15)*(5.5*(2*5.5**2)/8)*((-4.77*5.5**2)/8)),

        (vf.ParabolicTrapezoid(3, 3, -2, 2), vf.Rectangle(3, -2), -12.0),
        (vf.ParabolicTrapezoid(2.5, 2, 2.7, -1), vf.TriangleLeft(2.5, -2), -4.28125),
        (vf.ParabolicTrapezoid(2.5, 2, 2.7, -1), vf.TriangleRight(2.5, -2), -4.864583),
        (vf.ParabolicTrapezoid(2.5, 2, 2.7, -1), vf.Trapezoid(2.5, 2, -2), -0.58333333),
        (vf.ParabolicTrapezoid(2.5, 2, 2.7, -1), vf.Parabola(2.5, -1), -2.2460937499),
        (vf.ParabolicTrapezoid(9, 2, 2.7, -1), vf.ParabolicTrapezoid(9, 7.68, 99, 30), -12543.696),
    ],)


def test_pairs(fig1, fig2, expected):
    assert fig1+fig2 == pytest.approx(expected, rel=1e-6)

def test_add_mismatched_x_raises():
    fig1 = vf.Rectangle(5, 3)
    fig2 = vf.Rectangle(6, 3)  # różne x
    with pytest.raises(ValueError, match="x of figures doesn't match"):
        _ = fig1 + fig2


def test_integrate_pair_mismatched_x_raises():
    fig1 = vf.Parabola(3, 2)
    fig2 = vf.TriangleLeft(5, 2)  # różne x
    with pytest.raises(ValueError, match="x of figures doesn't match"):
        fig1 + fig2


def test_draw_situation_mismatched_x_raises():
    fig1 = vf.TriangleRight(2, 5)
    fig2 = vf.Trapezoid(3, 1, 2)  # różne x
    viz = VereshchaginVisualiser()
    with pytest.raises(ValueError, match="x of figures doesn't match"):
        viz.draw_situation(fig1, fig2)


@pytest.mark.parametrize("invalid_input", [
    "not_a_figure",
    123,
    None,
    3.14,
    object()
])
def test_add_invalid_type_raises(invalid_input):
    fig = vf.Rectangle(5, 2)
    with pytest.raises(TypeError, match=r"Unsupported figure type"):
        _ = fig + invalid_input


@pytest.mark.parametrize("invalid_input", [
    "not_a_figure",
    123,
    None,
    3.14,
    object()
])
def test_draw_figure_invalid_type_raises(invalid_input):
    viz = VereshchaginVisualiser()
    with pytest.raises(TypeError, match=r"Unsupported figure type"):
        viz.draw_figure(invalid_input)


@pytest.mark.parametrize("invalid_input", [
    "not_a_figure",
    123,
    None,
    3.14,
    object()
])
def test_integrate_pair_invalid_type_raises(invalid_input):
    fig = vf.Rectangle(5, 2)
    with pytest.raises(TypeError, match=r"Unsupported figure type"):
        _ = vf.integrate_pair(fig, invalid_input)