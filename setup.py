# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='sphinx-git-lowdown',
    version='0.0.1',
    url='https://github.com/yamahigashi/sphinx-git-lowdown',
    # download_url='http://pypi.python.org/pypi/sphinx-git-lowdown',
    license='Apache',
    author='yamahigashi',
    author_email='yamahigashi@gmail.com',
    description='Sphinx extension to wrap git changelog',
    long_description="",
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    include_package_data=True,
    install_requires=['Sphinx>=1.1', 'GitPython', 'lowdown'],
    # namespace_packages=['sphinx_git_lowdown'],
    packages=['sphinx_git_lowdown'],
)
