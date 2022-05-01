import config.project

package_name = config.project.project_name

console_scripts = [
    'tagger=pytags.tagger:main',
]

setup_requires = [
]

run_requires = [
    'pytconf',
    'pylogconf',
    "mysql.connector",
]

test_requires = [
    'pylint',
    'pytest',
    'pytest-cov',
    'pyflakes',
    'flake8',
]

dev_requires = [
    'pyclassifiers',
    'pypitools',
    'pydmt',
    'Sphinx',
    'pymakehelper',
]

install_requires = list(setup_requires)
install_requires.extend(run_requires)

extras_require = {
}

python_requires = ">=3.9"
test_os = [ "ubuntu-20.04" ]
test_python = [ "3.9" ]
test_container = [ "ubuntu:20.04" ]
