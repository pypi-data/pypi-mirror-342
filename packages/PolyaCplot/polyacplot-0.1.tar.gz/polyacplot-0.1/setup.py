from setuptools import setup, find_packages

setup(
    name="PolyaCplot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sympy",
        "matplotlib",
        "numpy",
        "pyvista"
    ],
)
