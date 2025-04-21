from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "numcurios.fast_math",
        sources=["cpp/fast_math.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++"
    )
]

setup(
    name="numcurios",
    version="0.1.0",
    description="Библиотека для работы с интересными числами и комбинаторикой",
    author="Твоё Имя",
    author_email="you@example.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    packages=["numcurios"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    zip_safe=False,
)
