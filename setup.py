#!/usr/bin/env python
from setuptools.command.install import install as _install
from setuptools import setup, find_packages, Command
import os, sys
import shutil
import ctypes.util
import configparser, platform
from shellpartycli import APP_VERSION

class generate_configuration_files(Command):
    description = "Generate configfiles from old files or SatoshiChaind config file"
    user_options = []

    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

    def run(self):
        from shellpartycli.setup import generate_config_files
        generate_config_files()

class install(_install):
    description = "Install shellparty-cli and dependencies"

    def run(self):
        caller = sys._getframe(2)
        caller_module = caller.f_globals.get('__name__','')
        caller_name = caller.f_code.co_name
        if caller_module == 'distutils.dist' or caller_name == 'run_commands':
            _install.run(self)
        else:
            self.do_egg_install()
        self.run_command('generate_configuration_files')

required_packages = [
    'appdirs',
    'prettytable',
    'colorlog',
    'python-dateutil',
    'requests',
    'shellparty-lib'
]

setup_options = {
    'name': 'shellparty-cli',
    'version': APP_VERSION,
    'author': 'Shellparty Foundation',
    'author_email': 'support@shellparty.io',
    'maintainer': 'Adam Krellenstein',
    'maintainer_email': 'adamk@shellparty.io',
    'url': 'http://shellparty.io',
    'license': 'MIT',
    'description': 'Shellparty Protocol Command-Line Interface',
    'long_description': '',
    'keywords': 'shellparty,SatoshiChain',
    'classifiers': [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Office/Business :: Financial",
        "Topic :: System :: Distributed Computing"
    ],
    'download_url': 'https://github.com/ShellpartySHP/shellparty-cli/releases/tag/v' + APP_VERSION,
    'provides': ['shellpartycli'],
    'packages': find_packages(),
    'zip_safe': False,
    'install_requires': required_packages,
    'setup_requires': required_packages,
    'entry_points': {
        'console_scripts': [
            'shellparty-client = shellpartycli:client_main',
            'shellparty-server = shellpartycli:server_main',
        ]
    },
    'cmdclass': {
        'install': install,
        'generate_configuration_files': generate_configuration_files
    }
}
# prepare Windows binaries
if sys.argv[1] == 'py2exe':
    import py2exe
    from py2exe.distutils_buildexe import py2exe as _py2exe

    WIN_DIST_DIR = 'shellparty-cli-win32-{}'.format(APP_VERSION)

    class py2exe(_py2exe):
        def run(self):
            from shellpartycli.setup import before_py2exe_build, after_py2exe_build
            # prepare build
            before_py2exe_build(WIN_DIST_DIR)
            # build exe's
            _py2exe.run(self)
            # tweak build
            after_py2exe_build(WIN_DIST_DIR)

    # Update setup_options with py2exe specifics options
    setup_options.update({
        'console': [
            'shellparty-client.py',
            'shellparty-server.py'
        ],
        'zipfile': 'library/site-packages.zip',
        'options': {
            'py2exe': {
                'dist_dir': WIN_DIST_DIR
            }
        },
        'cmdclass': {
            'py2exe': py2exe
        }
    })
# prepare PyPi package
elif sys.argv[1] == 'sdist':
    setup_options['long_description_markdown_filename'] = 'README.md'
    setup_options['setup_requires'].append('setuptools-markdown')

setup(**setup_options)
