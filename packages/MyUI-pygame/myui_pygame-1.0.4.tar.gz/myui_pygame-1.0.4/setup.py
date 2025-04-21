from setuptools import setup, find_packages

setup(
    name="MyUI_pygame",
    version="1.0.4",
    author="Neo Zetterberg",
    author_email="20091103neo@gmail.com",
    description="An easy-to-use extension to the very well-known package Pygame.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/MyUI",  # optional
    packages=find_packages(),
    install_requires=[
        "pygame",
        "pyperclip"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)