"""Test the get_package_root program."""

# Standard Library
import pathlib
from argparse import Namespace

# Third Party
import git
import pytest

# build-rez-packages-action
import get_package_root


def test_build_parser():
    """Test get_package_root.build_parser()."""
    parser = get_package_root.build_parser()

    expected = [action.dest for action in parser._actions[1:]]

    assert expected == ["root_parameter", "from_git", "tag"]


@pytest.mark.parametrize("tag", (None, "1.2.3"))
def test_checkout_git_repo(mocker, tag):
    """Test get_package_info.checkout_git_repo()."""
    mock_repo = mocker.MagicMock(spec=git.Repo)
    mock_clone = mocker.patch.object(get_package_root.Repo, "clone_from", return_value=mock_repo)

    mock_url = mocker.MagicMock(spec=str)
    mock_path = mocker.MagicMock(spec=pathlib.Path)

    get_package_root.checkout_git_repo(mock_url, mock_path, tag_name=tag)

    mock_clone.assert_called_once_with(mock_url, mock_path)

    if tag is not None:
        assert mock_repo.head.reference == mock_repo.tags[tag].commit
        mock_repo.head.reset.assert_called_with(index=True, working_tree=True)


@pytest.mark.parametrize(
    "git_url, git_tag",
    (
        ("", None),
        ("https://github.com/captainhammy/houdini-core-tools.git", None),
        ("https://github.com/captainhammy/houdini-core-tools.git", "1.2.3"),
    ),
)
def test_main(monkeypatch, tmp_path, mocker, git_url, git_tag):
    """Test get_package_root.main()."""
    monkeypatch.setenv("RUNNER_TEMP", tmp_path.as_posix())

    mock_checkout = mocker.patch("get_package_root.checkout_git_repo")

    expected_path = tmp_path / "houdini-core-tools"

    mock_namespace = mocker.MagicMock(spec=Namespace)
    mock_namespace.root_parameter = "."
    mock_namespace.from_git = git_url
    mock_namespace.tag = git_tag

    mock_parser = mocker.patch("get_package_root.argparse.ArgumentParser")
    mock_parser.return_value.parse_args.return_value = mock_namespace

    mock_write = mocker.patch("get_package_root.write_result")

    get_package_root.main()

    if git_url:
        mock_checkout.assert_called_with(git_url, expected_path, tag_name=git_tag)
        mock_write.assert_called_with(expected_path.as_posix())

    else:
        mock_write.assert_called_with(".")


def test_write_result(monkeypatch, tmp_path):
    """Test get_package_root.write_result()."""
    output_file = tmp_path / "test_output.txt"

    monkeypatch.setenv("GITHUB_OUTPUT", output_file.as_posix())

    expected = "/path/to/package_root/"

    get_package_root.write_result(expected)

    with output_file.open() as handle:
        assert handle.read() == f"package_root={expected}\n"
