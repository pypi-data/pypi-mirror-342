from setuptools import setup, find_packages

setup(
    name="gruvboxify",
    version="1.0.0",
    packages=find_packages(),
    install_requires = [
        "numpy>=2.2.2",
        "Pillow>=10.0.0"
    ],
    entry_points = {
        "console_scripts": [
            "gruvboxify = gruvboxify:main",
        ],
    }
)
