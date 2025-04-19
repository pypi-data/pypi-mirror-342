import sys
from os import path

from setuptools import find_packages, setup

TESTS_REQUIRE = []

# Mock is only required for Python 2
PY2 = sys.version_info[0] == 2

if PY2:
    TESTS_REQUIRE.append("mock>=2.0.0")

with open(path.join("attotime", "version.py")) as f:
    exec(f.read())

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, "README.rst")) as f:
    README_TEXT = f.read()

setup(
    name="attotime",
    version=__version__,
    description="Arbitrary precision datetime library.",
    long_description=README_TEXT,
    long_description_content_type="text/x-rst",
    author="Brandon Nielsen",
    author_email="nielsenb@jetfuse.net",
    url="https://codeberg.org/nielsenb-jf/attotime",
    packages=find_packages(),
    extras_require={
        "dev": TESTS_REQUIRE
        + [
            "black",
            "coverage",
            "isort",
            "pre-commit",
            "pyenchant",
            "pylint",
        ]
    },
    test_suite="attotime",
    tests_require=TESTS_REQUIRE,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="datetime decimal",
    project_urls={
        "Changelog": "https://codeberg.org/nielsenb-jf/attotime/src/branch/main/CHANGELOG.rst",
        "Documentation": "https://attotime.readthedocs.io",
        "Source": "https://codeberg.org/nielsenb-jf/attotime",
        "Tracker": "https://codeberg.org/nielsenb-jf/attotime/issues",
    },
)
