
from __future__ import annotations

import argparse
import pathlib
import os
from typing import TYPE_CHECKING

import rez.packages
from rez.utils.formatting import PackageRequest

if TYPE_CHECKING:
    from rez.developer_package import DeveloperPackage

import rez


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("variant")
    parser.add_argument("request")

    return parser


def get_package(package_root: pathlib.Path) -> DeveloperPackage:
    """Get the package from the local package.py folder.

    Args:
        package_root: The package directory.

    Returns:
        The package.
    """
    package = rez.packages.get_developer_package(package_root.as_posix())

    return package


def requests_match(request1: PackageRequest, request2: PackageRequest) -> bool:
    if request1.name != request2.name:
        return False

    return request1.range.intersects(request2.range)


def find_matching_variant(request_str: str) -> int:
    print(pathlib.Path.cwd())
    package = get_package(pathlib.Path.cwd())

    if not request_str:
        return -1

    request = PackageRequest(request_str)

    # package = get_package(pathlib.Path("/home/graham/src/houdini-toolbox-inlinecpp"))

    matching_indices = []

    for variant in package.iter_variants():
        for requires in variant.requires:
            if requests_match(requires, request):
                matching_indices.append(variant.index)

    if not matching_indices:
        return -1

    if len(matching_indices) > 1:
        raise RuntimeError("Too many options")

    return matching_indices[-1]


def write_result(package_variant: int) -> None:
    """Write the package name to the outputs file.

    Args:
        package_variant: The package variant.
    """
    has_variant = 1 if package_variant != -1 else 0

    output_path = pathlib.Path(os.environ["GITHUB_OUTPUT"])

    with output_path.open("a", encoding="utf-8") as fp:
        fp.write(f"has_variant={has_variant}\n")
        fp.write(f"variant_index={package_variant}\n")


def main():
    parser = build_parser()
    args = parser.parse_args()
    variant = args.variant
    request = args.request

    variant_idx = int(variant) if variant != '' else find_matching_variant(request)

    write_result(variant_idx)


if __name__ == "__main__":
    main()
