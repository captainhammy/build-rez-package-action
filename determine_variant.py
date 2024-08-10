"""Program to determine which variant, if any, to build."""

# Future
from __future__ import annotations

# Standard Library
import argparse
import os
import pathlib

# Third Party
import rez.packages
from rez.utils.formatting import PackageRequest


def build_parser() -> argparse.ArgumentParser:
    """Build the program's argument parser.

    Returns:
        The argument parser.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("variant")
    parser.add_argument("request")

    return parser


def find_matching_variant(request_str: str) -> int:
    """Find a variant matching the given request.

    This function returns the index of the variant.

    A return value of

    Args:
        request_str: A package request string.

    Returns:
        The index of the variant, if it exists.

    Raises:
        RuntimeError: If there are no match, or more than one variant matches the request.
    """
    request = PackageRequest(request_str)
    package = rez.packages.get_developer_package(pathlib.Path.cwd().as_posix())

    matching_indices = []

    for variant in package.iter_variants():
        matching_indices.extend([variant.index for requires in variant.requires if requests_match(requires, request)])

    if not matching_indices:
        raise RuntimeError("No matching variants match the request")  # noqa: TRY003

    if len(matching_indices) > 1:
        raise RuntimeError("More than one variant matches the request")  # noqa: TRY003

    return matching_indices[-1]


def requests_match(request1: PackageRequest, request2: PackageRequest) -> bool:
    """Check if two package requests match.

    Args:
        request1: A package request.
        request2: A package request.

    Returns:
        Whether two package requests match.
    """
    if request1.name != request2.name:
        return False

    return request1.range.intersects(request2.range)


def write_result(package_variant: int | None) -> None:
    """Write the package name to the outputs file.

    Args:
        package_variant: The package variant.
    """
    has_variant = 1 if package_variant is not None else 0

    if package_variant is None:
        package_variant = -1

    output_path = pathlib.Path(os.environ["GITHUB_OUTPUT"])

    with output_path.open("a", encoding="utf-8") as fp:
        fp.write(f"has_variant={has_variant}\n")
        fp.write(f"variant_index={package_variant}\n")


def main() -> None:
    """The program."""
    parser = build_parser()
    args = parser.parse_args()
    variant = args.variant
    request = args.request

    # If the variant value is not an empty string, use the integer value of it.
    # Otherwise, if the request value is empty, use None. If the value is set, try and
    # find a matching variant.
    variant_idx = int(variant) if variant else None if not request else find_matching_variant(request)

    write_result(variant_idx)


if __name__ == "__main__":
    main()
