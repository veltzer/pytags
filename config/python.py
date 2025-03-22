""" python depedencies for this project """
from typing import List


console_scripts: List[str] = [
    "tagger=pytags.tagger:main",
]
dev_requires: List[str] = [
    "pypitools",
]
config_requires: List[str] = [
    "pyclassifiers",
]
install_requires: List[str] = [
    "pytconf",
    "pylogconf",
    "mysql.connector",
]
build_requires: List[str] = [
    "pydmt",
    "pymakehelper",
]
test_requires: List[str] = [
    "pylint",
    "pytest",
    "pytest-cov",
    "pyflakes",
    "flake8",
    "mypy",
]
requires = config_requires + install_requires + build_requires + test_requires
