from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="flet-camera-webview",
    version="0.1.4",
    description="Камера для Flet через WebView",
    author="Риженков Олександр",
    author_email="you@example.com",
    url="https://github.com/yourusername/flet_camera",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"flet_camera": ["assets/*.html"]},
    install_requires=["flet", "flet_webview", "websockets"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
