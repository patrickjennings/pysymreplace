from collections import defaultdict
from operator import itemgetter
from pysymreplace.exceptions import NotSymlinkError, SameRelativePathsError
from pysymreplace.symlogger import logger

try:
    from pathlib import Path
except ImportError as e:
    from pathlib2 import Path


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
                    for symlink in self._get_symlinks_from_directory(file_path):
                        yield symlink

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

    def _order_symlinks_for_replacement(self, symlink_paths):
        resolved_path_mapping = {
            symlink_path: symlink_path.resolve()
            for symlink_path in symlink_paths
        }

        # Validate that two references are not referencing each other.
        resolved_paths = set(resolved_path_mapping.values())
        if len(resolved_path_mapping) != len(resolved_paths):
            duplicate_resolved_paths = _find_duplicates_values(resolved_path_mapping)
            message = 'Duplicate Paths: {}'.format(duplicate_resolved_paths)
            raise SameRelativePathsError(message)

        return sorted(
            resolved_path_mapping,
            key=resolved_path_mapping.__getitem__,
            reverse=True
        )

    def replace_symlink_with_target(self, symlink_path):
        symlink_path = Path(symlink_path)
        target_path = symlink_path.resolve()

        if not self._dry_run:
            self._replace(symlink_path, target_path)

        logger.debug('%s -> %s', target_path, symlink_path)

    def replace_symlinks_with_target(self, symlink_paths):
        symlink_paths = (Path(symlink_path) for symlink_path in symlink_paths)
        ordered_symlink_paths = self._order_symlinks_for_replacement(symlink_paths)

        for symlink_path in ordered_symlink_paths:
            self.replace_symlink_with_target(symlink_path)


def _find_duplicates_values(mapping):
    multi_dict = defaultdict(list)
    for key, value in mapping.items():
        multi_dict[value].append(key)

    return [
        value_list
        for key, value_list in multi_dict.items()
        if len(value_list) > 1
    ]
