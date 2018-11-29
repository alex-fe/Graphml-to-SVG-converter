from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='graphml2svg',
    url='https://github.com/alex-fe/Graphml-to-SVG-converter',
    author='Alex Feldman',
    author_email='alexfeldman93@gmail.com',
    packages=['graphml2svg'],
    install_requires=['svgwrite'],
    version='0.0.3',
    license='MIT',
    description='YFile .graphml converter to .svg',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
