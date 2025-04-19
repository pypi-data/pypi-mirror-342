import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from typing import Union, Callable, Optional

import matplotlib
matplotlib.use('TkAgg')


def grid(
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        density: int | tuple[int, int]
) -> tuple[np.ndarray, np.ndarray]:
    """
    get a coordinate grid for an image

    :param x_range: Range of x-axis values.
    :param y_range: Range of y-axis values.
    :param density: Number of grid points per axis for vector field.

    :return: grid coordinates for real and imaginary parts.
    """
    x_min, x_max = x_range
    y_min, y_max = y_range

    step_x = (x_max - x_min) / density
    step_y = (y_max - y_min) / density

    x = np.linspace(x_min - step_x / 2, x_max + step_x / 2, density, endpoint=True, retstep=False, dtype=None, axis=0)
    y = np.linspace(y_min - step_y / 2, y_max + step_x / 2, density, endpoint=True, retstep=False, dtype=None, axis=0)

    X, Y = np.meshgrid(x, y, indexing='xy', sparse=False, copy=True)

    return X, Y


def get_func(
        f_expr: Union[sp.Expr, Callable[[np.ndarray], np.ndarray]],
        z: sp.Symbol = None
) -> Callable:
    """
    get a function

    :param f_expr: Expression representing the complex function f(z).
    :param z: Symbol representing the complex variable z.

    :return: function
    """
    if callable(f_expr):
        return f_expr
    else:
        return sp.lambdify(z, f_expr, "numpy")


def vectorplot(
        f_expr: sp.Expr | Callable[[np.ndarray], np.ndarray],
        z: sp.Symbol = None,
        ax: Optional[plt.Axes] = None,
        x_range: tuple[float, float] = (-1, 1),
        y_range: tuple[float, float] = (-1, 1),
        density: int = 25,
        colormap: str = "plasma",
        add_colorbar: bool = False,
        quiver_kwargs: dict = None
) -> None:
    """
    Plots the Polya vector field for a complex function f(z).

    :param f_expr: Expression representing the complex function f(z).
    :param z: Symbol representing the complex variable z.
    :param ax: Axes that used to construct a plot.
    :param x_range: Range of x-axis values, default is (-1, 1).
    :param y_range: Range of y-axis values, default is (-1, 1).
    :param density: Number of grid points per axis for vector field, default is 25.
    :param colormap: Color of the streamplot, default is "plasma".
    :param quiver_kwargs: parameters for plt.quiver.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    X, Y = grid(x_range, y_range, density)
    Z = X + Y * 1j

    func = get_func(f_expr, z)
    result = func(Z)

    u, v = result.real, -result.imag
    magnitude = np.sqrt(u ** 2 + v ** 2)
    U = u / (magnitude + 1e-7)
    V = v / (magnitude + 1e-7)

    if quiver_kwargs is None:
        quiver_kwargs = dict(
            pivot='mid',
            headwidth=4,
            headlength=5,
            headaxislength=4.5,
            width=0.0025,
            alpha=0.8
        )

    q = ax.quiver(X, Y, U, V, magnitude, cmap=colormap, **quiver_kwargs)

    if add_colorbar:
        fig.colorbar(q, ax=ax)


def streamplot(
        f_expr: sp.Expr | Callable[[np.ndarray], np.ndarray],
        z: sp.Symbol = None,
        ax: Optional[plt.Axes] = None,
        x_range: tuple[float, float] = (-1, 1),
        y_range: tuple[float, float] = (-1, 1),
        density: int = 25,
        streamline_density: tuple[int, int] | int = (2, 2),
        colormap: str = "plasma",
        add_colorbar: bool = False,
        streamplot_kwargs: dict = None
) -> None:
    """
    Plots the streamplot for a complex function f(z) by Polya vector field.

    :param f_expr: Expression representing the complex function f(z).
    :param z: Symbol representing the complex variable z.
    :param ax: Axes that used to construct a plot.
    :param x_range: Range of x-axis values, default is (-1, 1).
    :param y_range: Range of y-axis values, default is (-1, 1).
    :param density: Number of grid points per axis for streamplot, default is 25.
    :param streamline_density: Density of the streamlines, default is (2, 2).
    :param colormap: Color of the streamplot, default is "plasma".
    :param streamplot_kwargs: parameters for plt.streamplot.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    X, Y = grid(x_range, y_range, density)
    Z = X + Y * 1j

    func = get_func(f_expr, z)
    result = func(Z)

    u, v = result.real, -result.imag
    magnitude = np.sqrt(u ** 2 + v ** 2)

    if streamplot_kwargs is None:
        streamplot_kwargs = dict(
            linewidth=1,
            arrowsize=1,
            arrowstyle='->'
        )

    ax.streamplot(X, Y, u, v, color=magnitude, cmap=colormap, density=streamline_density, **streamplot_kwargs)

    if add_colorbar:
        import matplotlib.cm as cm
        sm = cm.ScalarMappable(cmap=colormap)
        sm.set_array(magnitude)
        fig.colorbar(sm, ax=ax)


def zeros(
        f_expr: sp.Expr,
        z: sp.Symbol,
        ax: Optional[plt.Axes] = None,
        x_range: tuple[float, float] = (-1, 1),
        y_range: tuple[float, float] = (-1, 1),
        scatter_kwargs: dict = None
) -> None:
    """
    highlights zeros in the plot

    :param f_expr: Expression representing the complex function f(z).
    :param z: Symbol representing the complex variable z.
    :param ax: Axes that used to construct a plot.
    :param x_range: Range of x-axis values, default is (-1, 1).
    :param y_range: Range of y-axis values, default is (-1, 1).
    :param scatter_kwargs: parameters for plt.scatter.
    """

    if not isinstance(f_expr, sp.Expr):
        raise TypeError("Zero detection is supported only for sympy expressions.")

    if ax is None:
        ax = plt.gca()

    zeros_sym = sp.solve(f_expr, z)
    zeros = []

    for zero in zeros_sym:
        zero_val = sp.N(zero)
        re_zero = float(sp.re(zero_val))
        im_zero = float(sp.im(zero_val))

        if x_range[0] <= re_zero <= x_range[1] and y_range[0] <= im_zero <= y_range[1]:
            zeros.append((re_zero, -im_zero))

    if zeros:
        zeros_re, zeros_im = zip(*zeros)
        if scatter_kwargs is None:
            scatter_kwargs = dict(
                color='red',
                s=50,
                marker='o',
                alpha=0.75
            )
        ax.scatter(zeros_re, zeros_im, label="zeros", **scatter_kwargs)


def poles(
        f_expr: sp.Expr,
        z: sp.Symbol,
        ax: Optional[plt.Axes] = None,
        x_range: tuple[float, float] = (-1, 1),
        y_range: tuple[float, float] = (-1, 1),
        scatter_kwargs: dict = None
) -> None:
    """
    highlights poles in the plot

    :param f_expr: Expression representing the complex function f(z).
    :param z: Symbol representing the complex variable z.
    :param ax: Axes that used to construct a plot.
    :param x_range: Range of x-axis values, default is (-1, 1).
    :param y_range: Range of y-axis values, default is (-1, 1).
    :param scatter_kwargs: parameters for plt.scatter.
    """
    if not isinstance(f_expr, sp.Expr):
        raise TypeError("Pole detection is supported only for sympy expressions.")

    if ax is None:
        ax = plt.gca()

    f_expr_simpl = sp.together(sp.simplify(f_expr))
    num, den = sp.fraction(f_expr_simpl)
    poles_sym = sp.solve(den, z)
    poles = []

    for sol in poles_sym:
        sol_val = sp.N(sol)
        re_val = float(sp.re(sol_val))
        im_val = float(sp.im(sol_val))

        if x_range[0] <= re_val <= x_range[1] and y_range[0] <= im_val <= y_range[1]:
            poles.append((re_val, im_val))

    if poles:
        poles_re, poles_im = zip(*poles)
        if scatter_kwargs is None:
            scatter_kwargs = dict(
                color='blue',
                s=50,
                marker='x',
                alpha=0.75
            )
        ax.scatter(poles_re, poles_im, label="Poles", **scatter_kwargs)


def grid_deformation(
        f_expr : sp.Expr | Callable[[np.ndarray], np.ndarray],
        z : sp.Symbol = None,
        ax: Optional[plt.Axes] = None,
        x_range: tuple[float, float] = (-1, 1),
        y_range: tuple[float, float] = (-1, 1),
        density: int = 25
) -> None:
    '''
    Deforms the coordinate grid by the function f(z) and plots it

    :param f_expr: Expression representing the complex function f(z).
    :param z: Symbol representing the complex variable z.
    :param ax: Axes that used to construct a plot.
    :param x_range: Range of x-axis values, default is (-1, 1).
    :param y_range: Range of y-axis values, default is (-1, 1).
    :param density: Density of the grid, default is 25.
    '''
    if ax is None:
        ax = plt.gca()

    X, Y = grid(x_range, y_range, density)
    Z = X + Y * 1j

    func = get_func(f_expr, z)
    result = func(Z)

    u, v = result.real, -result.imag

    levels_real = np.linspace(np.min(X), np.max(X), density)
    levels_imag = np.linspace(np.min(Y), np.max(Y), density)

    ax.contour(u, v, X, levels=levels_real, colors='grey', linestyles='solid', alpha=0.3)
    ax.contour(u, v, Y, levels=levels_imag, colors='grey', linestyles='solid', alpha=0.3)

    x_min, x_max = max(np.min(X), np.min(u)), min(np.max(X), np.max(u))
    y_min, y_max = max(np.min(Y), np.min(-v)), min(np.max(Y), np.max(-v))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
