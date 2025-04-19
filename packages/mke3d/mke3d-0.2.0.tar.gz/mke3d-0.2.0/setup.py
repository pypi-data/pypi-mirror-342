from setuptools import setup, find_packages

setup(
    name="mke3d",
    version="0.2.0",
    author="Mk Smlv",
    author_email="me@mk-samoilov.ru",
    description="Basic 3D Engine with OpenGL",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mk-samoilov/3D-Engine",
    packages=find_packages(),
    install_requires=["PyOpenGL", "pygame", "numpy", "Pillow", "glfw", "imgui"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
