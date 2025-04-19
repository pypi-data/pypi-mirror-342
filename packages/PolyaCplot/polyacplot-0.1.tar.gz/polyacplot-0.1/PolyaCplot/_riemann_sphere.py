import numpy as np
import sympy as sp
import PolyaCplot as pc
import pyvista as pv
from typing import Callable


def stereographic_projection_from_north(
        z : np.ndarray
):
    """
    Stereographic projection from the north pole.
    It is used to display z points from the plane (South chart).

    :param z: array of complex numbers

    :return: array of projected points
    """
    X = np.real(z)
    Y = np.imag(z)

    denom = 1 + np.abs(z) ** 2
    sph_x = 2 * X / denom
    sph_y = 2 * Y / denom
    sph_z = (np.abs(z) ** 2 - 1) / denom

    return sph_x, sph_y, sph_z


def stereographic_projection_from_south(
        w : np.ndarray
):
    """
    Stereographic projection from the south pole.
    It is used to display w points from the inverse plane (North chart).
    In this case, w = 0 goes to the north pole.

    :param w: array of complex numbers in the plane

    :return: array of projected points
    """
    X = np.real(w)
    Y = np.imag(w)

    denom = 1 + np.abs(w) ** 2
    sph_x = 2 * X / denom
    sph_y = 2 * Y / denom
    sph_z = (1 - np.abs(w) ** 2) / denom

    return sph_x, sph_y, sph_z


def compute_tangent_vectors(z, u, v, projection='north'):
    """
    Computes the tangent vectors (dX/dx, dX/dy, dX/dz, dY/dx, dY/dy, dY/dz, dZ/dx, dZ/dy, dZ/dz)
    for a given point (z, u, v) on the Riemann sphere.

    :param z: complex number in the plane
    :param u: normalized real component of the vector field in the plane.
    :param v: normalized imaginary component of the vector field in the plane.
    :param projection: 'north' or 'south'

    :return: array of tangent vectors
    """
    X = np.real(z)
    Y = np.imag(z)

    denom = 1 + X ** 2 + Y ** 2

    if projection == 'north':
        # Стандартная стереографическая проекция
        dXdx = 2 / denom - 4 * X ** 2 / denom ** 2
        dXdy = -4 * X * Y / denom ** 2
        dYdx = -4 * X * Y / denom ** 2
        dYdy = 2 / denom - 4 * Y ** 2 / denom ** 2
        dZdx = 4 * X / denom ** 2
        dZdy = 4 * Y / denom ** 2
    else:
        # Стереографическая проекция из южного полюса
        dXdx = 2 / denom - 4 * X ** 2 / denom ** 2
        dXdy = -4 * X * Y / denom ** 2
        dYdx = -4 * X * Y / denom ** 2
        dYdy = 2 / denom - 4 * Y ** 2 / denom ** 2
        dZdx = -4 * X / denom ** 2
        dZdy = -4 * Y / denom ** 2

    dX = dXdx * u + dXdy * v
    dY = dYdx * u + dYdy * v
    dZ = dZdx * u + dZdy * v
    return dX, dY, dZ


def riemann_vectorplot(
        f_expr: sp.Expr | Callable[[np.ndarray], np.ndarray],
        z: sp.Symbol,
        density: int = 40,
        colormap: str = "plasma",
        max_magnitude: float = 1000.0
):
    """
    Plots the vector field for a complex function f(z) on the Riemann sphere.

    :param f_expr: Expression representing the complex function f(z).
    :param z_sym: Symbol representing the complex variable z.
    :param density: Number of grid points per axis for vector plot, default is 40.
    :param colormap: Color of the vector plot, default is "plasma".
    :param max_magnitude: Maximum magnitude of the vector field, default is 1000.
    """
    X, Y = pc.grid(x_range=(-1, 1), y_range=(-1, 1), density=density)
    Z = X + 1j * Y

    mask_south = np.abs(Z) <= 1 + 1e-3
    Z_filtered = Z[mask_south]

    f = pc.get_func(f_expr, z)
    result = f(Z_filtered)

    U = np.real(result)
    V = -np.imag(result)
    magnitude = np.sqrt(U ** 2 + V ** 2)

    magnitude = np.clip(magnitude, None, max_magnitude)

    u = U / (magnitude + 1e-7)
    v = V / (magnitude + 1e-7)

    sx, sy, sz = stereographic_projection_from_north(Z_filtered)
    pts_south = np.vstack([sx.flatten(), sy.flatten(), sz.flatten()]).T

    dX_s, dY_s, dZ_s = compute_tangent_vectors(Z_filtered, u, v, projection='north')
    vecs_south = np.vstack([dX_s.flatten(), dY_s.flatten(), dZ_s.flatten()]).T
    mags_south = magnitude.flatten()

    # ====================================================================================

    W1, W2 = pc.grid(x_range=(-1, 1), y_range=(-1, 1), density=density)
    w = W1 + 1j * W2

    mask_north = np.abs(w) <= 1 + 1e-3
    w_filtered = w[mask_north]

    g = pc.get_func(f_expr, z)
    result_w = g(1 / w_filtered)

    result_w = (-1 / (w_filtered**2)) * result_w
    U_w = np.real(result_w)
    V_w = -np.imag(result_w)
    magnitude_w = np.sqrt(U_w ** 2 + V_w ** 2)

    magnitude_w = np.clip(magnitude_w, None, max_magnitude)

    u_w = U_w / (magnitude_w + 1e-7)
    v_w = V_w / (magnitude_w + 1e-7)

    sx_w, sy_w, sz_w = stereographic_projection_from_south(w_filtered)
    pts_north = np.vstack([sx_w.flatten(), sy_w.flatten(), sz_w.flatten()]).T

    dX_w, dY_w, dZ_w = compute_tangent_vectors(w_filtered, u_w, v_w, projection='south')
    vecs_north = np.vstack([dX_w.flatten(), dY_w.flatten(), dZ_w.flatten()]).T
    mags_north = magnitude_w.flatten()

    # ====================================================================================

    pts_all = np.vstack([pts_south, pts_north])
    vecs_all = np.vstack([vecs_south, vecs_north])
    mags_all = np.hstack([mags_south, mags_north])

    grid = pv.PolyData(pts_all)
    grid["vectors"] = vecs_all
    grid["magnitude"] = mags_all

    arrows = grid.glyph(orient="vectors", scale=False, factor=0.1)

    p = pv.Plotter()

    sphere = pv.Sphere(radius=1.0, theta_resolution=50, phi_resolution=50)
    p.add_mesh(sphere, color="lightgrey", opacity=0.5)

    p.add_mesh(arrows, scalars="magnitude", cmap=colormap, lighting=True)
    p.show()
