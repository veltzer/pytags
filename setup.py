import setuptools

setuptools.setup(
    name='pytags',
    version='0.0.7',
    description='module to help you tag interesting places in your code',
    long_description='module to help you tag interesting places in your code',
    url='https://veltzer.github.io/pytags',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='pytags tag code command line',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    entry_points={
        'console_scripts': [
            'tagger=pytags.tagger:main',
        ],
    },
)
