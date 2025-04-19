from setuptools import setup, find_packages

setup(
    name="get_lunchbox",  # unikalna nazwa (PyPI nie pozwoli na 'textutils')
    version="1.0" , # Potem 1.1
    packages=find_packages(),
    install_requires=[],
    description="Useful tool for easy importing with aliases",
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