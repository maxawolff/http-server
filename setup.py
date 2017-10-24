"""Set up file for http-server."""

from setuptools import setup

setup(
    name="http-server",
    description="Simple server implemented in Python",
    package_dir={"": "src"},
    author="Max Wolff, Joseph Kim",
    author_email=["maxawolff@hotmail.com", "joseph.kim.kr@gmail.com"],
    py_modules=["client,", "server"],
    install_requires=[],
    extras_require={
        "test": ["pytest", "pytest-cov", "pytest-watch", "tox"],
        "development": ["ipython"]
    },
    entry_points={
    }
)
