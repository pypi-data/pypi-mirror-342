from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dsi-toolkit",
    version="1.0.7",
    author="Márcio Falcão dos Santos Barroso",
    author_email="barroso@ufsj.edu.br",
    description="The provided script 'dsi-toolkit' leverages a package designed for identifying polynomial models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jimjonessm/dsi_toolkit_examples/",
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
