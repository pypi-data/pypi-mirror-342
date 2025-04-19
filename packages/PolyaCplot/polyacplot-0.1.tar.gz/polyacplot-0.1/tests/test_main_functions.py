import pytest
import PolyaCplot as pc
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def test_grid_dimensions():
    x_range = (-2, 2)
    y_range = (-3, 3)
    density = 10

    X, Y = pc.grid(x_range, y_range, density)

    assert X.shape == (density, density)
    assert Y.shape == (density, density)

    step_x = (x_range[1] - x_range[0]) / density
    expected_min = x_range[0] - step_x / 2
    expected_max = x_range[1] + step_x / 2

    np.testing.assert_allclose(X[0, 0], expected_min, rtol=1e-3)
    np.testing.assert_allclose(X[-1, -1], expected_max, rtol=1e-3)


def test_get_func_lambda():
    f = lambda z: z**2
    func = pc.get_func(f)
    z_values = np.array([1 + 1j, 2 + 2j])

    np.testing.assert_allclose(func(z_values), f(z_values), rtol=1e-5)


def test_get_func_sympy():
    z = sp.symbols('z')
    expr = z ** 2
    func = pc.get_func(expr, z)
    test_vals = np.array([1 + 1j, 2 + 2j])
    expected = test_vals ** 2

    np.testing.assert_allclose(func(test_vals), expected, rtol=1e-5)


def test_streamplot():
    z = sp.symbols('z')
    f_expr = z ** 2

    fig, ax = plt.subplots()

    x_range = (-2, 2)
    y_range = (-2, 2)

    try:
        pc.streamplot(f_expr, z=z, ax=ax, x_range=x_range, y_range=y_range, density=50)
    except Exception as e:
        pytest.fail(f"streamplot raised an exception: {e}")
    finally:
        plt.close(fig)

    plt.show()


def test_zeros_and_poles():
    z = sp.symbols('z')

    expr = (z - 1) / (z + 2)
    fig, ax = plt.subplots()
    try:
        pc.zeros(expr, z, ax=ax, x_range=(-5, 5), y_range=(-5, 5))
        pc.poles(expr, z, ax=ax, x_range=(-5, 5), y_range=(-5, 5))
    except Exception as e:
        pytest.fail(f"zeros or poles function raised an exception: {e}")
    finally:
        plt.close(fig)


def test_grid_deformation():
    z = sp.symbols('z')
    f_expr = z ** 2

    fig, ax = plt.subplots()

    x_range = (-2, 2)
    y_range = (-2, 2)

    try:
        pc.grid_deformation(f_expr, z=z, ax=ax, x_range=x_range, y_range=y_range, density=50)
    except Exception as e:
        pytest.fail(f"streamplot raised an exception: {e}")
    finally:
        plt.close(fig)

    plt.show()


def test_streamplot_with_sliders(
        x_range=(-10, 10),
        y_range=(-10, 10),
        density=20,
        colormap="plasma"
):
    z = sp.symbols('z')
    f_expr = 1 / z ** 2

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(12, 6))
    plt.subplots_adjust(bottom=0.25)

    plt.sca(ax_left)
    pc.streamplot(f_expr, z, x_range=x_range, y_range=y_range, density=density, colormap=colormap)
    ax_left.set_title("Функция 1/z^2")

    a_init = 1
    f_2 = 1 / (z ** 2 - a_init ** 2)
    plt.sca(ax_right)

    pc.streamplot(f_2, z, x_range=x_range, y_range=y_range, density=density, colormap=colormap)
    ax_right.set_title("функция 1/(z^2 - a^2)")

    ax_slider = plt.axes((0.25, 0.1, 0.65, 0.03))
    slider = Slider(ax_slider, 'a', 0, 10, valinit=a_init, valstep=1)

    def update(val):
        a = int(slider.val)
        ax_right.clear()
        plt.sca(ax_right)
        f_new = 1 / (z ** 2 - a ** 2)
        pc.streamplot(f_new, z, x_range=x_range, y_range=y_range, density=density, colormap=colormap)
        ax_right.set_title("функция 1/(z ** 2 - a^2)")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()


def test_streamplot_with_sliders_2(
        x_range=(-10, 10),
        y_range=(-10, 10),
        density=20,
        colormap="plasma"
):
    z = sp.symbols('z')
    f_expr = 1 / z ** 3

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(12, 6))
    plt.subplots_adjust(bottom=0.25)

    plt.sca(ax_left)
    pc.streamplot(f_expr, z, x_range=x_range, y_range=y_range, density=density, colormap=colormap)
    ax_left.set_title("Функция 1/z^3")

    a_init = 1
    f_2 = 1 / (z ** 3 - a_init ** 3)
    plt.sca(ax_right)

    pc.streamplot(f_2, z, x_range=x_range, y_range=y_range, density=density, colormap=colormap)
    ax_right.set_title("функция 1/(z^3 - a^3)")

    ax_slider = plt.axes((0.25, 0.1, 0.65, 0.03))
    slider = Slider(ax_slider, 'a', 0, 10, valinit=a_init, valstep=1)

    def update(val):
        a = int(slider.val)
        ax_right.clear()
        plt.sca(ax_right)
        f_new = 1 / (z ** 3 - a ** 3)
        pc.streamplot(f_new, z, x_range=x_range, y_range=y_range, density=density, colormap=colormap)
        ax_right.set_title("функция 1/(z ** 3 - a^3)")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()
