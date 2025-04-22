from setuptools import setup, find_packages
from codecs import open
from os import path

# taken from https://tom-christie.github.io/articles/pypi/
here = path.abspath(path.dirname(__file__))

# taken from https://tom-christie.github.io/articles/pypi/
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='traicionar',
    version='0.0.2',
    url='https://github.com/montoyamoraga/traicionar.py',
    author='montoyamoraga',
    license='MIT',
    description='library for electronic betrayal',
    long_description='library for electronic betrayal',
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    programming_language='Python',

)