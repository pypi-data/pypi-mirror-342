import os
from setuptools import setup, find_packages
from pathlib import Path


__DIRNAME__ = os.path.dirname(os.path.abspath(__file__))
BASE_PACKAGE = "bbrowserx_connector"
BASE_IMPORT = "bbrowserx_connector"


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def _install_requires():
    with open(os.path.join(__DIRNAME__, "requirements.txt"), "r", encoding="utf-8") as rf:
        return list(map(str.strip, rf.readlines()))


setup(
    name=BASE_PACKAGE,
    version="1.0.0",
    author="BioTuring",
    author_email="support@bioturing.com",
    url="https://alpha.bioturing.com",
    description="BioTuring BBrowserX Connector",
    package_dir={BASE_IMPORT: "bbrowserx_connector"},
    packages=[BASE_IMPORT, *find_packages()],
    zip_safe=False,
    install_requires=_install_requires(),
    long_description=long_description,
    long_description_content_type="text/markdown",
)
