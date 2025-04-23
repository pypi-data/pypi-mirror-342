from setuptools import Extension, setup
from os import getenv

args = []

env_var_value = getenv("ECCLIB_DEBUG")
if env_var_value == "1":
    args.extend(["-O0", "-ggdb3", "-Wall", "-Wextra"])
elif env_var_value:
    args.extend(["-O3"])

module1 = Extension(
    "eccLib",
    sources=[
        "src/eccLib.c",
        "src/common.c",
        "src/functions.c",
        "src/formats/fasta.c",
        "src/formats/gtf.c",
        "src/classes/GtfDict.c",
        "src/classes/GtfReader.c",
        "src/classes/GeneList.c",
        "src/classes/FastaBuff.c",
        "src/hashmap_ext.c",
        "xxHash/xxhash.c",
    ],
    include_dirs=["src", "xxHash"],  # this doesnt work for sdist, thats why MANIFEST.in
    extra_compile_args=args,
)

setup(
    name="eccLib",
    version="1.0.0",
    description="Library for parsing FASTA and GTF files",
    url="https://gitlab.platinum.edu.pl/eccdna/eccLib",
    author="Tomasz Chady",
    author_email="tomek.chady@gmail.com",
    python_requires=">=3.10",
    ext_modules=[module1],
    packages=["eccLib"],
    package_dir={"eccLib": "./stub"},
    package_data={"eccLib": ["__init__.pyi"]},
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: C",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
)

# to compile and install this library run the following commands:
# pip install .
# Python will do it's thing just fine :)
