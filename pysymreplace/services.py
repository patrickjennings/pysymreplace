from itertools import permutations
from pathlib import Path
from pysymreplace.exceptions import NotSymlinkError, SameRelativePathsError
from pysymreplace.logging import logger


class SymlinkFinderService:
    """
    Finds symbolic link paths from a list of file paths.
    """
    def __init__(self, follow_symlinks=True):
        self._follow_symlinks = follow_symlinks

    def _validate_symlink(self, file_path):
        if not file_path.is_symlink():
            raise NotSymlinkError(file_path)
        return file_path

    def _get_symlinks_from_directory(self, directory):
        for file_path in directory.rglob('*'):
            try:
                yield self._validate_symlink(file_path)
            except NotSymlinkError:
                if file_path.is_dir():
                    yield from self._get_symlinks_from_directory(file_path)

    def find_symlinks(self, file_paths):
        symlink_paths = set()
        for file_path in file_paths:
            file_path = Path(file_path)

            if file_path.is_symlink():
                symlink_paths.add(file_path)

                if not self._follow_symlinks:
                    continue

            if file_path.is_dir():
                new_symlink_paths = self._get_symlinks_from_directory(file_path)
                symlink_paths.update(new_symlink_paths)

        return symlink_paths


class SymlinkReplacerService:
    """
    Replaces symbolic links with the original file.
    """
    def __init__(self, dry_run=False):
        self._dry_run = dry_run

    def _replace(self, source_path, target_path):
        # Cannot move a directory to a file
        if target_path.is_dir():
            source_path.unlink()

        # Replace target with source
        target_path.rename(source_path)

    def _validate_symlinks(self, symlink_paths):
        resolved_paths = (
            Path(symlink_path).resolve() for symlink_path in symlink_paths
        )

        # Validate that the two references are not relative to each other.
        for first_path, second_path in permutations(resolved_paths, 2):
            try:
                first_path.relative_to(second_path)
            except ValueError as e:
                pass
            else:
                message = '{} & {}'.format(first_path, second_path)
                raise SameRelativePathsError(message)

    def replace_symlink_with_target(self, symlink_path):
        symlink_path = Path(symlink_path)
        target_path = symlink_path.resolve()

        if not self._dry_run:
            self._replace(symlink_path, target_path)

        logger.debug('%s -> %s', target_path, symlink_path)

    def replace_symlinks_with_target(self, symlink_paths):
        self._validate_symlinks(symlink_paths)
        for symlink_path in symlink_paths:
            self.replace_symlink_with_target(symlink_path)
