"""Setup configuration for ScreenClicker library."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="screenclicker",
    version="0.1.0",
    author="ScreenClicker Development Team",
    description="Minimal screen automation library for Wayland/Linux systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
    ],
    python_requires=">=3.6",
    install_requires=[
        "python-uinput>=1.0.1",
    ],
    keywords="automation, wayland, mouse, keyboard, gui, testing",
    project_urls={
        "Bug Reports": "https://github.com/olavbm/screenclicker/issues",
        "Source": "https://github.com/olavbm/screenclicker",
    },
)