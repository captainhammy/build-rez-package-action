"""Test the get_package_info program."""

# Standard Library
from argparse import Namespace

# Third Party
import pytest

# build-rez-packages-action
import get_package_info


def test_build_parser():
    """Test get_package_info.build_parser()."""
    parser = get_package_info.build_parser()

    expected = [option.lstrip("-") for action in parser._actions[-1:] for option in action.option_strings]

    assert expected == ["variant"]


@pytest.mark.parametrize(
    "variant,expected_variant",
    (
        (None, "''"),
        ("2", "2"),
    ),
)
def test_main(mocker, shared_datadir, variant, expected_variant):
    """Test get_package_info.main()."""
    mocker.patch("pathlib.Path.cwd", return_value=shared_datadir)

    mock_namespace = mocker.MagicMock(spec=Namespace)
    mock_namespace.variant = variant

    mock_parser = mocker.patch("get_package_info.argparse.ArgumentParser")
    mock_parser.return_value.parse_args.return_value = mock_namespace

    mock_write = mocker.patch("get_package_info.write_result")

    get_package_info.main()

    mock_write.assert_called_with("test_package", "0.3.0", expected_variant)


def test_write_result(monkeypatch, tmp_path):
    """Test get_package_info.write_result()."""
    output_file = tmp_path / "test_output.txt"

    monkeypatch.setenv("GITHUB_OUTPUT", output_file.as_posix())

    get_package_info.write_result("test_package", "0.2.0", "2")

    with output_file.open() as handle:
        assert handle.read() == "package_name=test_package\npackage_version=0.2.0\npackage_variant=2\n"
