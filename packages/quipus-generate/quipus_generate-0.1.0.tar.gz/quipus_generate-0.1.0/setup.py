from setuptools import setup, find_packages

setup(
    name="quipus-generate",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "quipus-generate=project.cli:main",
        ],
    },
    install_requires=[
        "inflection"
    ],
    description="Generador de proyectos FastAPI con arquitectura Hexagonal.",
    author="Juan Corrales",
    author_email="sistemas@amauttasistems.com",
)
