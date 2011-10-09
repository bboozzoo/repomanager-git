#!/usr/bin/env python

from distutils.core import setup

setup (
    name = 'repomanager',
    description = 'Simple wrappers for repository management',
    long_description = 'Simple wrappes for repository management with a web frontend. Current support is for git only',
    version = '0.0.1',
    author = 'Maciek Borzecki',
    author_email = 'maciek.borzecki@gmail.com',
    license = 'GPL',
    scripts = ['repomanager-git'],
    py_modules = [ 'repomanager_git', 'repgit', 'utils'],
    data_files = [('/etc/repomanager', ['repomanager.conf'])]
    )
