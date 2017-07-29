import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pytags',
    version='0.0.9',
    description='module to help you tag interesting places in your code',
    long_description='module to help you tag interesting places in your code',
    url='https://veltzer.github.io/pytags',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='pytags tag code command line',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'tagger=pytags.tagger:main',
        ],
    },
)
