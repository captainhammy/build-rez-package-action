"""Dummy package.py file for build testing"""

name = "test_install_package_with_variants"
version = "0.0.1"

build_system = "cmake"

variants = [
    ["six-1.14.0"],
    ["six-1.15.0"],
]


def commands():
    pass
