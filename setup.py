from setuptools import find_packages, setup

setup(
    name='mlb_learning',
    packages=find_packages(include=['mlb_learning']),
    version='0.0.1',
    description='MLB Learning',
    author='M.Moretti, S.Pradier',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.2'],    
)