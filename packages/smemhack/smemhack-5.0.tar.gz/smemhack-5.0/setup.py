from setuptools import setup, find_packages

setup(
    name="smemhack",
    version="5.0",
    packages=find_packages(),
    install_requires=[
        "tensorflow",
        "pyautogui",
        "pyperclip",
        "numpy"
    ],
    description="A Python library to automate online homework tasks with AI and system control.",
    author="Dickily",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",  # Minimum required Python version
)
