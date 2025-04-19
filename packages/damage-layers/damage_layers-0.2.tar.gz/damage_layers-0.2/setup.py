
from setuptools import setup, find_packages

setup(
    name='damage_layers',
    version='0.2',
    description='Damage-aware dense layers for neural networks',
    author='Mustafa Ekmekçi',
    author_email='mustafa.ekmekci@comu.edu.tr',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0'
    ],
)
