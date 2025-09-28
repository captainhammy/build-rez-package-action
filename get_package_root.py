"""Program to determine the actual package root."""

# Future
from __future__ import annotations

# Standard Library
import argparse
import os
import pathlib
from urllib.parse import urlparse

# Third Party
from git import Repo


def build_parser() -> argparse.ArgumentParser:
    """Build the program's argument parser.

    Returns:
        The argument parser.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("root_parameter")
    parser.add_argument("from_git")
    parser.add_argument("--tag", default=None)

    return parser


def checkout_git_repo(git_url: str, target_dir: pathlib.Path, tag_name: str | None = None) -> None:
    """Checkout the git repo at the given URL.

    Args:
        git_url: The girt repo URL.
        target_dir: The directory to clone the repo to.
        tag_name: Optional tag name.
    """
    target_dir.unlink(missing_ok=True)
    repo = Repo.clone_from(git_url, target_dir)

    if tag_name is not None:
        repo.head.reference = repo.tags[tag_name].commit
        repo.head.reset(index=True, working_tree=True)


def write_result(package_root: str) -> None:
    """Write the package name to the outputs file.

    Args:
        package_root: The package variant.
    """
    output_path = pathlib.Path(os.environ["GITHUB_OUTPUT"])

    with output_path.open("a", encoding="utf-8") as fp:
        fp.write(f"package_root={package_root}\n")


def main() -> None:
    """The program."""
    parser = build_parser()
    args = parser.parse_args()
    root_parameter = args.root_parameter
    url = args.from_git

    if url:
        parsed_url = urlparse(url)
        repo_name = os.path.splitext(os.path.basename(parsed_url.path))[0]

        git_path = pathlib.Path(os.environ["RUNNER_TEMP"]) / repo_name
        checkout_git_repo(url, git_path, tag_name=args.tag)

        write_result(git_path.as_posix())

    else:
        write_result(root_parameter)


if __name__ == "__main__":
    main()
