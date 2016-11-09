import io
import re
from setuptools import setup, find_packages


setup(
    name="rig_cpp_common",
    version="0.1.0",
    packages=find_packages(),

    # Metadata for PyPi
    url="https://github.com/project-rig/rig_cpp_common",
    author="University of Manchester",
    description="Common C++ and python code for applications built using Rig",
    #long_description=replace_local_hyperlinks(read_file("README.rst")),
    license="GPLv2",
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Science/Research",

        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",

        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",

        "Topic :: Scientific/Engineering",
    ],
    keywords="spinnaker c++",

    # Requirements
    install_requires=["rig>=2.0.0, <3.0.0",
                      "bitarray>=0.8.1, <1.0.0"],
    zip_safe=False,  # Partly for performance reasons

    # Scripts
    entry_points={
        "console_scripts": [
            "rig_cpp_common_path = rig_cpp_common.scripts.rig_cpp_common_path:main",
        ],
    },
)
