from argparse import ArgumentParser
from collections import namedtuple


Argument = namedtuple('Argument', ['type', 'keywords'])


class CLIArgumentParser:
    cli_description = 'Replaces all symbolic links with its target.'
    cli_arguments = (
        Argument('file_paths', {
                'metavar': 'SOURCE',
                'nargs': '+',
                'type': str,
                'help': 'Source path to recursively replace symlinks with their targets.'
            }
        ),
        # TODO: implement follow symlink argument
        # TODO: implement dry run
    )

    @property
    def file_paths(self):
        return self._arguments.file_paths

    def __init__(self, args=None):
        parser = ArgumentParser(description=self.cli_description)
        self._initialize_parser(parser)
        self._arguments = parser.parse_args(args)

    def _initialize_parser(self, parser):
        for argument in self.cli_arguments:
            parser.add_argument(argument.type, **argument.keywords)
