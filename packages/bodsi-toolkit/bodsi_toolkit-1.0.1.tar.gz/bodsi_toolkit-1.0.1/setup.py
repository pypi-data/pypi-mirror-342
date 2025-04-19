from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bodsi-toolkit",
    version="1.0.1",
    author="Márcio Falcão dos Santos Barroso",
    author_email="barroso@ufsj.edu.br",
    description="Bi-objective system identification using Polynomial NARX models minimizes dynamic and static errors via Pareto-optimal solutions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jimjonessm/bodsi_toolkit_examples/",
    license="Proprietary",  # Specify the license as 'Proprietary' (as per your custom license)
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Proprietary",  # Keep it simple, and mention the license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
