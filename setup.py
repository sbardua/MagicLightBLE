from setuptools import setup
from magiclightble import __version__

setup(
    name='magiclightble',
    version=__version__,
    description='Python module for controlling MagicLight '
                'BLE/Bluetooth Smart light bulbs',
    long_description=open('README.md').read(),
    url='https://github.com/sbardua/MagicLightBLE',
    author='Scott Bardua',
    author_email='sbardua@gmail.com',
    license='MIT',
    packages=['magiclightble'],
    install_requires=[
        'bluepy'
    ]
)
