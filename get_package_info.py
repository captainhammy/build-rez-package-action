"""Program to write package info to the action output."""

# Future
from __future__ import annotations

# Standard Library
import argparse
import os
import pathlib

# Third Party
import rez.packages


def build_parser() -> argparse.ArgumentParser:
    """Build the program's argument parser.

    Returns:
        The argument parser.
    """
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


def main() -> None:
    """The program."""
    parser = build_parser()
    args = parser.parse_args()
    variant = args.variant

    package = rez.packages.get_developer_package(pathlib.Path.cwd().as_posix())

    package_variant = variant if variant is not None else "''"

    write_result(package.name, str(package.version), package_variant)


if __name__ == "__main__":
    main()
