import PolyaCplot as pc
import sympy as sp


if __name__ == '__main__':
    z = sp.symbols('z')
    f_expr = z ** 2

    pc.riemann_vectorplot(f_expr, z, density=30, colormap="plasma", max_magnitude=1000.0)
