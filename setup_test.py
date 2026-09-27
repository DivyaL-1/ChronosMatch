from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "order_book",
        ["src/order_book.pyx"],
        language="c++",
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": 3},
    )
)
