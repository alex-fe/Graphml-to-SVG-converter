from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='graphml2svg',
    url='https://github.com/alex-fe/Graphml-to-SVG-converter',
    author='Alex Feldman',
    author_email='alexfeldman93@gmail.com',
    # Needed to actually package something
    packages=['converter'],
    # Needed for dependencies
    install_requires=['svgwriter'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='YFile .graphml converter to .svg',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.md').read(),
)
