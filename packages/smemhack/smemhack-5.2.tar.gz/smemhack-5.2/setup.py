from setuptools import setup, find_packages

# Load README content for PyPI description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smemhack",
    version="5.2",
    packages=find_packages(),
    install_requires=[
        "tensorflow",
        "pyautogui",
        "pyperclip",
        "numpy"
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
    python_requires=">=3.6",  # Minimum required Python version
)
