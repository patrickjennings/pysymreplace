import pytest
from pysymreplace.cli import CLIArgumentParser


@pytest.mark.parametrize('arguments', [
    ['/path/to/symlinks/'],
    ['/path/to/symlinks/', '/another/path'],
])
def test_cli_arguments(arguments):
    parser = CLIArgumentParser(arguments)
    assert parser.file_paths == arguments


def test_cli_missing_arguments():
    with pytest.raises(SystemExit):
        CLIArgumentParser()
