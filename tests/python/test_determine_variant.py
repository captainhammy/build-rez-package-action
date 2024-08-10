"""Test the determine_variant program."""

# Standard Library
from argparse import Namespace
from contextlib import nullcontext

# Third Party
import pytest
from rez.utils.formatting import PackageRequest

# build-rez-packages-action
import determine_variant


def test_build_parser():
    """Test get_package_info.build_parser()."""
    parser = determine_variant.build_parser()

    expected = [action.dest for action in parser._actions[-2:]]

    assert expected == ["variant", "request"]


@pytest.mark.parametrize(
    "request1,request2,expected",
    (
        (PackageRequest("foo-123"), PackageRequest("bar-456"), False),
        (PackageRequest("houdini-20.0"), PackageRequest("houdini-20.5"), False),
        (PackageRequest("houdini-20.5"), PackageRequest("houdini-20.5"), True),
    ),
)
def test_requests_match(request1, request2, expected):
    """Test get_package_info.requests_match()."""
    assert determine_variant.requests_match(request1, request2) == expected


@pytest.mark.parametrize(
    "request_str,expected,context",
    (
        ("foo", -1, pytest.raises(RuntimeError, match="No matching variants match the request")),
        ("six", -1, pytest.raises(RuntimeError, match="More than one variant matches the request")),
        ("six-1.15", 1, None),
    ),
)
def test_find_matching_variant(mocker, shared_datadir, request_str, expected, context):
    """Test determine_variant.find_matching_variant()."""
    mocker.patch("pathlib.Path.cwd", return_value=shared_datadir)

    if context is None:
        context = nullcontext()

    with context:
        result = determine_variant.find_matching_variant(request_str)

        assert result == expected


@pytest.mark.parametrize(
    "variant,req,expected_index",
    (
        ("", "", None),
        ("", "foo-2", 4),
        ("2", "foo-3", 2),
    ),
)
def test_main(mocker, shared_datadir, variant, req, expected_index):
    """Test determine_variant.main()."""
    mocker.patch("pathlib.Path.cwd", return_value=shared_datadir)

    mock_namespace = mocker.MagicMock(spec=Namespace)
    mock_namespace.variant = variant
    mock_namespace.request = req

    mock_parser = mocker.patch("determine_variant.argparse.ArgumentParser")
    mock_parser.return_value.parse_args.return_value = mock_namespace

    mocker.patch("determine_variant.find_matching_variant", return_value=4)
    mock_write = mocker.patch("determine_variant.write_result")

    determine_variant.main()

    mock_write.assert_called_with(expected_index)


@pytest.mark.parametrize(
    "variant,expected",
    (
        (None, 0),
        (2, 1),
    ),
)
def test_write_result(monkeypatch, tmp_path, variant, expected):
    """Test determine_variant.write_result()."""
    output_file = tmp_path / "test_output.txt"

    monkeypatch.setenv("GITHUB_OUTPUT", output_file.as_posix())

    determine_variant.write_result(variant)

    with output_file.open() as handle:
        assert handle.read() == f"has_variant={expected}\nvariant_index={variant if variant is not None else -1}\n"
