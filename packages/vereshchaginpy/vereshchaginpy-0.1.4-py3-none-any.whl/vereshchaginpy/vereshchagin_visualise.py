import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from . import vereshchagin_figures as vf
from .vereshchagin_pairs import get_figure_pair_type, FigureType


class VereshchaginVisualiser:

    """
    Optional utility class for visualizing figure combinations involved in the integration process.

    This class provides a graphical interface for plotting two geometric figures that are subject
    to integration. It helps in understanding how the shapes interact and how their combination
    contributes to the resulting integral. Colors, alpha blending, annotations, and layout are
    handled automatically depending on the type of figures provided.

    Instances of this class expose the methods `draw_situation(...)`,and draw_figure(...) for plotting
    one or two figures, respectively. The figures are expected to be instances of the VereshchaginFigures.
    """

    def draw_figure(self, figure):
        """
        Displays a single figure on a standalone plot.

        Useful for quickly visualizing the shape, parameters, and annotations
        of a single object (e.g., Rectangle, TriangleLeft, Parabola, etc.).

        Args:
            figure: The figure object to display.
        """

        vf.validate_figure(figure)
        fig, ax = plt.subplots()

        self._draw_single(ax, figure, color='blue', alpha=0.4, label_offset=0)

        # Set proper y-limits
        heights = []
        if hasattr(figure, "height"):
            heights.append(figure.height)
        elif hasattr(figure, "height_left") and hasattr(figure, "height_right"):
            heights.extend([figure.height_left, figure.height_right])
        else:
            heights.append(0)

        min_y = min(0, *heights)
        max_y = max(0, *heights)
        padding = (max_y - min_y) * 0.2 or 1
        ax.set_ylim(min_y - padding, max_y + padding)

        ax.axhline(0, color='black', linewidth=1)
        ax.set_xlim(0, figure.x)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.title(f'Figure: {type(figure).__name__}')
        plt.show()

    def draw_situation(self, figure_1, figure_2):
        """
        Displays a visual representation of the interaction between two figures on a shared plot.

        Based on the types of the input figures, the correct rendering logic is applied
        using the internal `_draw_single` method. Annotations, colors, layout, and axis
        scaling are handled automatically.

        Args:
            figure_1: The first figure to display.
            figure_2: The second figure to display.
        """
        vf.validate_figure(figure_1)
        vf.validate_figure(figure_2)

        if figure_1.x != figure_2.x:
            raise ValueError(f"x of figures doesn't match: x1 = {figure_1.x}, x2 = {figure_2.x}")

        fig, ax = plt.subplots()
        self._draw_pair(ax, figure_1, figure_2)

        heights = []
        for fig in [figure_1, figure_2]:
            if hasattr(fig, "height"):
                heights.append(fig.height)
            elif hasattr(fig, "height_left") and hasattr(fig, "height_right"):
                heights.extend([fig.height_left, fig.height_right])
            else:
                heights.append(0)

        min_y = min(0, *heights)
        max_y = max(0, *heights)
        padding = (max_y - min_y) * 0.2 or 1
        ax.set_ylim(min_y - padding, max_y + padding)

        ax.axhline(0, color='black', linewidth=1)
        ax.set_xlim(0, figure_1.x)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.title(f'Situation: {type(figure_1).__name__} + {type(figure_2).__name__}')
        plt.show()

    def _draw_single(self, ax, fig, color, alpha, label_offset=0.0):

        """
        Internal method for drawing a single figure onto a given Matplotlib axis.

        This method handles all supported figure types and applies appropriate geometry,
        shading, and annotations. Not intended to be called directly by users — use
        `draw_figure(...)` instead.

        Args:
            ax: The Matplotlib axis to draw on.
            fig: The figure object to render.
            color: The fill color for the figure.
            alpha: The transparency level for the fill.
            label_offset: Vertical or horizontal offset applied to labels for clarity.
        """

        x0 = 0

        match fig:
            case vf.Rectangle(x=x, height=h):
                y0 = min(0, h)
                ax.add_patch(
                    patches.Rectangle((x0, y0), x, abs(h), color=color, alpha=alpha)
                )
                y_label = h + 0.2 + label_offset if h >= 0 else h - 0.2 - label_offset
                ax.text(x0 + x / 2, y_label, f"rectangle height = {h}",
                        ha='center', va='bottom' if h >= 0 else 'top')
                ax.text(x0 + x / 2, -0.3, f"x = {x}", ha='center', va='top')

            case vf.TriangleLeft(x=x, height=h):
                ax.add_patch(
                    patches.Polygon([(x0, 0), (x0, h), (x0 + x, 0)], closed=True, color=color, alpha=alpha)
                )
                direction = 1 if h >= 0 else -1
                x_label = x0 - 0.3 - label_offset * direction
                ax.text(x_label, h / 2, f"triangle height = {h}",
                        ha='right', va='center', rotation=90)
                ax.text(x0 + x / 2, -0.3, f"x = {x}", ha='center', va='top')

            case vf.TriangleRight(x=x, height=h):
                ax.add_patch(
                    patches.Polygon([(x0, 0), (x0 + x, h), (x0 + x, 0)], closed=True, color=color, alpha=alpha)
                )
                direction = 1 if h >= 0 else -1
                x_label = x0 + x + 0.3 + label_offset * direction
                ax.text(x_label, h / 2, f"triangle height = {h}",
                        ha='left', va='center', rotation=90)
                ax.text(x0 + x / 2, -0.3, f"x = {x}", ha='center', va='top')

            case vf.Trapezoid(x=x, height_left=h_left, height_right=h_right):
                ax.add_patch(
                    patches.Polygon(
                        [(x0, 0), (x0, h_left), (x0 + x, h_right), (x0 + x, 0)],
                        closed=True, color=color, alpha=alpha
                    )
                )

                direction_left = 1 if h_left >= 0 else -1
                direction_right = 1 if h_right >= 0 else -1

                ax.text(x0 - 0.3 - label_offset * direction_left, h_left / 2,
                        f"hL = {h_left}", ha='right', va='center', rotation=90)

                ax.text(x0 + x + 0.3 + label_offset * direction_right, h_right / 2,
                        f"hR = {h_right}", ha='left', va='center', rotation=90)

                ax.text(x0 + x / 2, -0.3, f"x = {x}", ha='center', va='top')

            case vf.Parabola(x=x, line_load=load):
                f = (load * x ** 2) / 8
                self._draw_parabola_through_points(
                    ax,
                    x1=0,
                    x2=x,
                    ymax=f,
                    color=color,
                    alpha=alpha,
                    label=f"parabola f = {round(f, 2)}"
                )
                ax.text(x / 2, -0.3, f"x = {x}", ha='center', va='top')
            case vf.ParabolicTrapezoid(x=x, height_left=h_left, height_right=h_right, line_load=line_load):
                f = (line_load * x ** 2) / 8

                x_vals = np.linspace(x0, x0 + x, 200)
                base_line = np.linspace(h_left, h_right, 200)
                bump = np.sin(np.linspace(0, np.pi, 200))
                curvature = f * 0.2
                y_vals = base_line + bump * curvature

                cross_axis = (h_left >= 0 and h_right <= 0) or (h_left <= 0 and h_right >= 0)

                if cross_axis:
                    ax.fill_between(x_vals, 0, y_vals, color=color, alpha=alpha)
                    ax.plot(x_vals, y_vals, color=color, linewidth=2, alpha=alpha)
                    peak_x = x0 + x / 2
                    peak_y = max(y_vals) if f >= 0 else min(y_vals)
                    ax.text(peak_x, peak_y + 0.2 if f >= 0 else peak_y - 0.2,
                            f"f = {round(f, 2)}", ha='center', va='bottom' if f >= 0 else 'top')

                else:
                    if f >= 0 and not (h_left < 0 and h_right < 0):
                        points = (
                                [(x0, 0)] +
                                list(zip(x_vals, y_vals)) +
                                [(x0 + x, 0)]
                        )
                        ax.add_patch(
                            patches.Polygon(points, closed=True, color=color, alpha=alpha)
                        )
                    else:
                        points = (
                                [(x0, 0)] +
                                list(zip(x_vals, y_vals)) +
                                [(x0 + x, 0)]
                        )
                        ax.add_patch(
                            patches.Polygon(points, closed=True, color=color, alpha=alpha)
                        )

                    ax.plot(x_vals, y_vals, color=color, linewidth=2, alpha=alpha)
                    peak_x = x0 + x / 2
                    peak_y = (h_left + h_right) / 2 + curvature
                    ax.text(peak_x, peak_y + 0.2 if f >= 0 else peak_y - 0.2,
                            f"f = {round(f, 2)}", ha='center', va='bottom' if f >= 0 else 'top')

                ax.text(x0 - 0.3, h_left / 2, f"hL = {h_left}", ha='right', va='center', rotation=90)
                ax.text(x0 + x + 0.3, h_right / 2, f"hR = {h_right}", ha='left', va='center', rotation=90)
                ax.text(x0 + x / 2, -0.3, f"x = {x}", ha='center', va='top')

            case _:
                raise TypeError(f"Unsupported figure type in overlay: {type(fig).__name__}")

    def _draw_pair(self, ax, fig1, fig2):

        """
        Internal helper to draw a standard pair of figures on the same axis.

        Args:
            ax: Matplotlib axis to draw on.
            fig1: First figure object (drawn in blue).
            fig2: Second figure object (drawn in red).
        """
        self._draw_single(ax, fig1, 'blue', 0.4, label_offset=0)
        self._draw_single(ax, fig2, 'red', 0.4, label_offset=0.5)

    def _draw_parabola_through_points(self, ax, x1, x2, ymax, color, alpha, label):

        """
        Internal helper for drawing a parabola that passes through two x-zeros and a given peak.

        Constructs a quadratic curve defined by three points: two zeros and a vertex.
        Used by other drawing methods for visualizing parabolic shapes.

        Not intended for direct use outside the class.

        Args:
            ax: The Matplotlib axis to draw on.
            x1: The first x-position (zero point).
            x2: The second x-position (zero point).
            ymax: The y-value at the vertex (peak of the parabola).
            color: The line and fill color.
            alpha: The transparency level of the fill.
            label: Text label to annotate the vertex.
        """

        xv = (x1 + x2) / 2
        A = np.array([
            [x1 ** 2, x1, 1],
            [x2 ** 2, x2, 1],
            [xv ** 2, xv, 1]
        ])
        b = np.array([0, 0, ymax])
        a, b, c = np.linalg.solve(A, b)

        x_vals = np.linspace(x1, x2, 200)
        y_vals = a * x_vals ** 2 + b * x_vals + c

        ax.plot(x_vals, y_vals, color=color, linewidth=2)
        ax.fill_between(x_vals, 0, y_vals, color=color, alpha=alpha)

        ax.text(xv, ymax + 0.2 if ymax >= 0 else ymax - 0.2, label,
                ha='center', va='bottom' if ymax >= 0 else 'top')
