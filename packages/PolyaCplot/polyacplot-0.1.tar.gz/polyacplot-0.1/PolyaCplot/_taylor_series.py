import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from ._main import streamplot

from typing import Optional, Callable
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

import matplotlib
matplotlib.use('Qt5Agg')


def taylor_poly(
        f_expr : sp.Expr | Callable[[np.ndarray], np.ndarray],
        var : sp.Symbol,
        n_terms : int
) -> sp.Expr:
    """
    get a taylor polynomial

    :param f_expr: Expression representing the complex function f(z).
    :param var: Symbol representing the complex variable z.
    :param n_terms: Number of terms in the taylor polynomial.

    :return: simplified taylor polynomial
    """
    poly = 0

    for k in range(n_terms + 1):
        term = f_expr.diff(var, k).subs(var, 0) / sp.factorial(k) * var**k
        poly += term

    return sp.simplify(poly)


def maclaurin_series(
        f_expr: sp.Expr | Callable[[np.ndarray], np.ndarray],
        z: sp.Symbol,
        fig: Figure,
        ax: Optional[plt.Axes] = None,
        x_range: tuple[float, float] = (-1, 1),
        y_range: tuple[float, float] = (-1, 1),
        density: int | float = 25,
        colormap: str = "plasma",
        n_init: int = 5,
        n_min: int = 3,
        n_max: int = 20,
        n_step: int = 1
) -> None:
    """
    Plots the maclaurin series for a complex function f(z) with a slider to control the number of terms.

    :param f_expr: Expression representing the complex function f(z).
    :param z: Symbol representing the complex variable z.
    :param fig: Figure that used to construct a plot.
    :param ax: Axes that used to construct a plot.
    :param x_range: Range of x-axis values, default is (-5, 5).
    :param y_range: Range of y-axis values, default is (-5, 5).
    :param density: Number of grid points per axis for streamplot, default is 25.
    :param colormap: Color of the streamplot, default is "plasma".
    :param n_init: Initial number of terms in Taylor series, default is 5.
    :param n_min: Minimum number of terms in Taylor series, default is 3.
    :param n_max: Maximum number of terms in Taylor series, default is 20.
    :param n_step: Step size for slider, default is 1.
    """
    if n_min < 2:
        raise ValueError("Minimum number of terms in Taylor series should be at least 2.")

    if ax is None:
        ax = plt.gca()

    taylor_expr = taylor_poly(f_expr, z, n_init)
    streamplot(taylor_expr, z, ax, x_range=x_range, y_range=y_range, density=density, colormap=colormap)

    ax_slider = plt.axes([0.1, 0.02, 0.8, 0.05])
    slider = Slider(ax_slider, 'n', n_min , n_max, valinit=n_init, valstep=n_step)

    def update(val):
        n = int(slider.val)
        ax.clear()
        new_taylor_expr = taylor_poly(f_expr, z, n)
        streamplot(new_taylor_expr, z, ax, x_range=x_range, y_range=y_range, density=density, colormap=colormap)
        fig.canvas.draw_idle()

    slider.on_changed(update)
