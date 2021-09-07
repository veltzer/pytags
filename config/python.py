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
]

test_requires = [
    'pylint',
    'pytest',
    'pyflakes',
]

dev_requires = [
    'pyclassifiers',
    'pypitools',
    'pydmt',
    'Sphinx',
]

install_requires = list(setup_requires)
install_requires.extend(run_requires)

python_requires = ">=3.6"

extras_require={
}
test_os = "[ubuntu-18.04, ubuntu-20.04]"
test_python = "[3.6, 3.7, 3.8]"
test_container = "[ 'ubuntu:18.04', 'ubuntu:20.04' ]"
