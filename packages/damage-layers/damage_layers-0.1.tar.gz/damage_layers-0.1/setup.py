
from setuptools import setup, find_packages

setup(
    name='damage_layers',
    version='0.1',
    description='Damage-aware dense layers for neural networks',
    author='Mucahit Atalan',
    author_email='example@example.com',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0'
    ],
)
