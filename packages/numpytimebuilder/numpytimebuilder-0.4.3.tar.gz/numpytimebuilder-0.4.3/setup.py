import sys
from os import path

from setuptools import find_packages, setup

NUMPY_REQUIREMENT = "numpy>=1.20.0"

PY2 = sys.version_info[0] == 2
PY39 = sys.version_info[0] == 3 and sys.version_info[1] == 9

if PY2:
    NUMPY_REQUIREMENT = "numpy<1.17.0"
elif PY39:
    NUMPY_REQUIREMENT = "numpy<2.1.0"

with open(path.join("numpytimebuilder", "version.py")) as f:
    exec(f.read())

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, "README.rst")) as f:
    README_TEXT = f.read()

setup(
    name="numpytimebuilder",
    version=__version__,
    description="A library for using the NumPy datetime API with aniso8601",
    long_description=README_TEXT,
    long_description_content_type="text/x-rst",
    author="Brandon Nielsen",
    author_email="nielsenb@jetfuse.net",
    url="https://codeberg.org/nielsenb-jf/numpytimebuilder",
    install_requires=["aniso8601>=9.0.0,<11.0.0", NUMPY_REQUIREMENT],
    extras_require={
        "dev": [
            "black",
            "coverage",
            "isort",
            "pre-commit",
            "pyenchant",
            "pylint",
        ]
    },
    packages=find_packages(),
    test_suite="numpytimebuilder",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="iso8601 numpy aniso8601 datetime",
    project_urls={
        "Changelog": "https://codeberg.org/nielsenb-jf/numpytimebuilder/src/branch/main/CHANGELOG.rst",
        "Documentation": "https://numpytimebuilder.readthedocs.io/",
        "Source": "https://codeberg.org/nielsenb-jf/numpytimebuilder",
        "Tracker": "https://codeberg.org/nielsenb-jf/numpytimebuilder/issues",
    },
)
