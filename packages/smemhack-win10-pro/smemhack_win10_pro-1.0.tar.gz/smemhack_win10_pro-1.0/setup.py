from setuptools import setup, find_packages

# Load README content for PyPI description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smemhack_win10_pro",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pyautogui>=0.9.53",      # Require PyAutoGUI version 0.9.53 or newer
        "pyperclip>=1.8.2",       # Require Pyperclip version 1.8.2 or newer
        "numpy>=1.20.0",          # Require NumPy version 1.20.0 or newer
        "keyboard>=0.13.5",       # Require Keyboard package version 0.13.5 or newer
        "fuzzywuzzy>=0.18.0",     # Require FuzzyWuzzy version 0.18.0 or newer
        "python-Levenshtein>=0.12.2"  # Require Python-Levenshtein version 0.12.2 or newer
    ],
    description="A Python library to automate online homework tasks with AI and system control.",
    long_description=long_description,  # Use README.md for the description
    long_description_content_type="text/markdown",  # Specify Markdown format for PyPI
    author="Dickily",
    author_email="dickilyyiu@gmail.com",  # Add your email for contact
    license="Proprietary",
    classifiers=[
        "License :: Other/Proprietary License",  # Proprietary license classifier
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.18",  # Require Python 3.8.18 or newer
)
