from setuptools import setup, find_packages

setup(
    name='UselessMath',
    version='0.0.1',
    description='A python library to do the most basic, useless math',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ricca665/UselessMath',
    author='Ricca665',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        # No depedencies
    ],
)