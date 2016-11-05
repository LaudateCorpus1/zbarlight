#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages, Extension
from distutils.command.build import build as DistutilsBuild

def read(file_path):
    with open(file_path) as fp:
        return fp.read()

class Build(DistutilsBuild):
    def run(self):
        cores_to_use = max(1, multiprocessing.cpu_count() - 1)
        cmd = ['./configure', '--disable-dependency-tracking', '--without-python', '--without-qt', '--disable-video', '--without-gtk', '--without-imagemagick', '--with-x=no']
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Could not build fastzbarlight: %s.\n" % e)
            raise

        cmd = ['make']
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Could not build fastzbarlight: %s.\n" % e)
            raise
        except OSError as e:
            sys.stderr.write("Unable to execute '{}'. HINT: are you sure `make` is installed?\n".format(' '.join(cmd)))
            raise
        DistutilsBuild.run(self)

setup(
    name='zbarlight',
    version='1.0.3.dev0',
    description="A simple zbar wrapper",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
    keywords=['zbar', 'QR code reader'],
    author='Polyconseil',
    author_email='opensource+zbarlight@polyconseil.fr',
    url='https://github.com/Polyconseil/zbarlight/',
    license='BSD',
    packages=find_packages(where='src', exclude=['docs', 'tests']),
    package_dir={'': str('src')},
    ext_modules=[
        Extension(
            name=str('zbarlight._zbarlight'),
            sources=[str('src/zbarlight/_zbarlight.c')],
            extra_compile_args=['-std=c99'],
            libraries=['zbar'],
            optional=os.environ.get('READTHEDOCS', False),  # Do not build on Read the Docs
        ),
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'setuptools',
    ],
    install_requires=[
        'Pillow',
    ],
)
