import logging
from pysymreplace.logging import initialize_logging, logger
from pysymreplace.cli import CLIArgumentParser
from pysymreplace.collections import SymlinkCollection
from pysymreplace.services import SymlinkReplacerService


def find_and_replace_symlinks(file_paths_to_search):
    # TODO: implement follow symlink argument
    symlink_paths = SymlinkCollection(file_paths_to_search)

    replacer_service = SymlinkReplacerService()
    replacer_service.replace_symlinks_with_target(symlink_paths)

    return symlink_paths


def main():
    initialize_logging(logging.DEBUG)

    cli_argument_parser = CLIArgumentParser()
    file_paths_to_search = cli_argument_parser.file_paths

    symlink_paths_replaced = find_and_replace_symlinks(file_paths_to_search)

    logger.info('Successfully replaced %s symlinks', len(symlink_paths_replaced))
