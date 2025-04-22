#!/usr/bin/env python
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class BuildExt(build_ext):
    def build_extensions(self):
        # Ensure C++11 is used
        # for ext in self.extensions:
        #     if '-std=c++11' not in ext.extra_compile_args:
        #         ext.extra_compile_args.append('-std=c++11')
        build_ext.build_extensions(self)

lzf_module = Extension(
    '_lzf',
    sources=['lzf.i', 'lzf.c', 'lz4.c'],
    include_dirs=['.'],
    swig_opts=['-modern'],
)

setup(
    name='lzf-python',
    version='1.0.4',
    description='Python bindings for LZF compression library',
    author='Author',
    author_email='author@example.com',
    url='https://github.com/author/lzf-python',
    ext_modules=[lzf_module],
    py_modules=['lzf'],
    cmdclass={'build_ext': BuildExt},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Compression',
    ],
    python_requires='>=3.6',
) 