import os
from glob import iglob
from pysymreplace.exceptions import NotSymlinkError
from pysymreplace.logging import logger


class SymlinkFinderService:
    """
    Finds symbolic link paths from a list of file paths.
    """
    def __init__(self, follow_symlinks=True):
        self._follow_symlinks = follow_symlinks

    def _validate_symlink(self, file_path):
        if not os.path.islink(file_path):
            raise NotSymlinkError(file_path)
        return file_path

    def _get_symlinks_from_directory(self, directory):
        path_pattern = '%s/*' % directory
        for file_path in iglob(path_pattern, recursive=True):
            try:
                yield self._validate_symlink(file_path)
            except NotSymlinkError:
                if os.path.isdir(file_path):
                    yield from self._get_symlinks_from_directory(file_path)

    def find_symlinks(self, file_paths):
        symlink_paths = set()
        for file_path in file_paths:
            if os.path.islink(file_path):
                new_symlink_path = self._validate_symlink(file_path)
                symlink_paths.add(new_symlink_path)

                if not self._follow_symlinks:
                    continue

            if os.path.isdir(file_path):
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
        if os.path.isdir(target_path):
            os.remove(source_path)

        # replace target with source
        os.replace(target_path, source_path)

    def replace_symlink_with_target(self, symlink_path):
        target_path = os.readlink(symlink_path)

        if not self._dry_run:
            self._replace(symlink_path, target_path)

        logger.debug('%s -> %s', target_path, symlink_path)

    def replace_symlinks_with_target(self, symlink_paths):
        for symlink_path in symlink_paths:
            self.replace_symlink_with_target(symlink_path)
