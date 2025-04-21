from setuptools import setup, find_packages
import codecs
import os
import toml

here = os.path.abspath(os.path.dirname(__file__))
pipfile_path = os.path.join(here, 'Pipfile')
readme_filename = os.path.join(here, 'README.md')

with codecs.open(readme_filename, encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

pipfile_data = toml.load(pipfile_path)

packages = pipfile_data.get('packages', {})
INSTALL_REQUIRES = [f"{pkg}{'' if spec == '*' else spec}" for pkg, spec in packages.items()]

VERSION = '0.1.4'
DESCRIPTION = 'A Python package that simplifies the process of building lead scoring models.'
PACKAGE_LICENSE = 'LICENSE.txt'

setup(
    name="glsm",
    version=VERSION,
    license=PACKAGE_LICENSE,
    author="Victor Valar",
    author_email="<valar@victorvalar.tech>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    keywords=['python', 'lead score', 'modeling', 'lead generation', 'lead scoring', 'lead scoring model'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
