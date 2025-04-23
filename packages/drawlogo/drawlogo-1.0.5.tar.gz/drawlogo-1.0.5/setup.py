from setuptools import setup, find_packages
from io import open
import os

version_module = {}
dir_name = os.path.dirname(__file__)
with open(os.path.join(dir_name, "src", "drawlogo", "version.py")) as fp:
    exec(fp.read(), version_module)
    __version__ = version_module['__version__']

with open(os.path.join(dir_name, "README.md"), encoding='utf8') as fh:
    long_description = fh.read()

# TODO add tests
setup(
    name='drawlogo',
    version=__version__,
    packages=find_packages('src'),
    include_package_data=True,
    package_data={'drawlogo': ['letters/*.svg']},
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'drawlogo=drawlogo.cli:main',
        ],
    },
    author="Sergey Abramov, Alexandr Boytsov",
    author_email='aswq22013@gmail.com',
    package_dir={'': 'src'},
    install_requires=[
        'docopt>=0.6.2',
        'numpy>=1.18.0',
        'schema>=0.7.2',
        'svgutils==0.3.1',
        'contextlib2>=0.5.5',
    ],
    extras_require={
        'dev': ['wheel', 'twine', 'setuptools_scm'],
    },
    python_requires='>=3.6',
    url="https://github.com/wish1/draw_motif_logo",
)
