import os
import setuptools

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(os.path.join(_ROOT, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="pgn2gif",
    version="1.0",
    description="Creates GIFs from PGNs",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Mehtab Zafar",
    url="https://github.com/mzfr/pgn2gif",
    packages=setuptools.find_packages(exclude=['pgn2gif/gifs']),
    install_requires=requirements,
    entry_points={'console_scripts': ['pgn2gif = pgn2gif:main']},
    keywords='pgn gifs',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities"
    ] + [('Programming Language :: Python :: %s' % x) for x in '3 3.4 3.5'.split()]
)
