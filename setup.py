from distutils.core import setup
from setuptools import find_packages

setup(name='tsapi',
      version='0.1',
      description='Python API for Teledrill MWD Tool Serial Communication',
      author='Kenneth Miller',
      author_email='xkenneth@gmail.com',
      packages = find_packages(),
      install_requires = ['setuptools',
                          'pyserial',
                          ]
     )
