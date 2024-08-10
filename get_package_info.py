
from __future__ import annotations

import argparse
import pathlib
import os
from typing import TYPE_CHECKING

import rez.packages

if TYPE_CHECKING:
    from rez.developer_package import DeveloperPackage


def get_package(package_root: pathlib.Path) -> DeveloperPackage:
    """Get the package from the local package.py folder.

    Args:
        package_root: The package directory.

    Returns:
        The package.
    """
    package = rez.packages.get_developer_package(package_root.as_posix())

    return package.name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("--variant", default=None)

    return parser


def write_result(package_name: str, package_version: str, package_variant: str) -> None:
    """Write the package name to the outputs file.

    Args:
        package_name: The local package name.
        package_version: The package version.
        package_variant: The package variant.
    """
    output_path = pathlib.Path(os.environ["GITHUB_OUTPUT"])

    with output_path.open("a", encoding="utf-8") as fp:
        fp.write(f"package_name={package_name}\n")
        fp.write(f"package_version={package_version}\n")
        fp.write(f"package_variant={package_variant}\n")


def main():

    parser = build_parser()
    args = parser.parse_args()
    variant = args.variant

    package = get_package(pathlib.Path.cwd())

    package_variant = variant if variant is not None else "''"

    write_result(package.name, package.version, package_variant)


if __name__ == "__main__":
    main()

