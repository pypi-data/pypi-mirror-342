import sympy as sp
import matplotlib.pyplot as plt
import PolyaCplot as pc


def test_cos_series():
    z = sp.symbols('z')
    f_expr = sp.cos(z)
    fig, ax = plt.subplots()
    pc.maclaurin_series(f_expr, z, fig, ax, x_range=(-5, 5), y_range=(-5, 5), n_init=5, n_min=2, n_max=20)
    plt.show()


def test_sin_series():
    z = sp.symbols('z')
    f_expr = sp.sin(z)
    fig, ax = plt.subplots()
    pc.maclaurin_series(f_expr, z, fig, ax, x_range=(-5, 5), y_range=(-5, 5), n_init=5, n_min=2, n_max=20)
    plt.show()


def test_exp_series():
    z = sp.symbols('z')
    f_expr = sp.exp(z)
    fig, ax = plt.subplots()
    pc.maclaurin_series(f_expr, z, fig, ax, x_range=(-5, 5), y_range=(-5, 5), n_init=5, n_min=2, n_max=20)
    plt.show()


def test_cos_series_with_orig():
    z = sp.symbols('z')
    f_expr = sp.cos(z)
    fig, (ax_1, ax_2) = plt.subplots(1, 2, figsize=(12, 6))
    pc.streamplot(f_expr, z, ax_1, x_range=(-5, 5), y_range=(-5, 5))
    pc.maclaurin_series(f_expr, z, fig, ax_2, x_range=(-5, 5), y_range=(-5, 5), n_init=5, n_min=2, n_max=20)
    plt.show()


def test_sin_series_with_orig():
    z = sp.symbols('z')
    f_expr = sp.sin(z)
    fig, (ax_1, ax_2) = plt.subplots(1, 2, figsize=(12, 6))
    pc.streamplot(f_expr, z, ax_1, x_range=(-5, 5), y_range=(-5, 5))
    pc.maclaurin_series(f_expr, z, fig, ax_2, x_range=(-5, 5), y_range=(-5, 5), n_init=5, n_min=2, n_max=20)
    plt.show()


def test_exp_series_with_orig():
    z = sp.symbols('z')
    f_expr = sp.exp(z)
    fig, (ax_1, ax_2) = plt.subplots(1, 2, figsize=(12, 6))
    pc.streamplot(f_expr, z, ax_1, x_range=(-5, 5), y_range=(-5, 5))
    pc.maclaurin_series(f_expr, z, fig, ax_2, x_range=(-5, 5), y_range=(-5, 5), n_init=5, n_min=2, n_max=20)
    plt.show()