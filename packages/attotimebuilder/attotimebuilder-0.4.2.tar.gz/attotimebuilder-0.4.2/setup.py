from os import path

from setuptools import find_packages, setup

with open(path.join("attotimebuilder", "version.py")) as f:
    exec(f.read())

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, "README.rst")) as f:
    README_TEXT = f.read()

setup(
    name="attotimebuilder",
    version=__version__,
    description="A library for using the attotime datetime API with aniso8601",
    long_description=README_TEXT,
    long_description_content_type="text/x-rst",
    author="Brandon Nielsen",
    author_email="nielsenb@jetfuse.net",
    url="https://codeberg.org/nielsenb-jf/attotimebuilder",
    install_requires=["aniso8601>=9.0.0, <11.0.0", "attotime>=0.2.2, <0.3.0"],
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
    test_suite="attotimebuilder",
    classifiers=[
        "Development Status :: 4 - Beta",
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
    keywords="iso8601 attotime aniso8601 datetime",
    project_urls={
        "Changelog": "https://codeberg.org/nielsenb-jf/attotimebuilder/src/branch/main/CHANGELOG.rst",
        "Documentation": "https://attotimebuilder.readthedocs.io/",
        "Source": "https://codeberg.org/nielsenb-jf/attotimebuilder",
        "Tracker": "https://codeberg.org/nielsenb-jf/attotimebuilder/issues",
    },
)
