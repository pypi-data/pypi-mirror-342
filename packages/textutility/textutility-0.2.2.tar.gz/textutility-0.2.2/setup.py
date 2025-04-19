from setuptools import setup, find_packages

setup(
    name="textutility",  # unikalna nazwa (PyPI nie pozwoli na 'textutils')
    version="0.2.2" , # Potem 0.2.5
    packages=find_packages(),
    install_requires=[],
    description="Useful string and text manipulation tools",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Carlos",
    author_email="karlos.santana13@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
