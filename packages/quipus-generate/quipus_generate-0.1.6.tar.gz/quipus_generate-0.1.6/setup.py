from setuptools import setup, find_packages

setup(
    name="quipus-generate",
    version="0.1.6",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "quipus-generate=amautta_project.cli:main",
        ],
    },
    install_requires=[
        "inflection"
    ],
    description="Generador de proyectos FastAPI con arquitectura Hexagonal.",
    author="Juan David Corrales Saldarriaga",
    author_email="sistemas@amauttasistems.com",
    license="Proprietary",
    include_package_data=True,
)
