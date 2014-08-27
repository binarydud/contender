from setuptools import setup, find_packages
setup(
    name='contender',
    version='0.2.1',
    author='Matt George',
    author_email='mgeorge@gmail.com',
    url='http://github.com/binarydud/contender',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'click',
        'github3.py',
        'six'
    ],
    tests_require=[
        'pytest',
        'pretend',
        'pytest-cov',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: System',
        'Topic :: System :: Software Distribution',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'contender = contender.commands:contender',
        ],
    },
)
