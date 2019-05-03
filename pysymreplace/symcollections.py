from pysymreplace.services import SymlinkFinderService

try:
    from collections.abc import Set
except ImportError as e:
    from collections import Set



class SymlinkCollection(Set):

    def __init__(self, *file_paths_to_search):
        symlink_finder_service = SymlinkFinderService()
        self._symlink_paths = symlink_finder_service.find_symlinks(file_paths_to_search)

    def __iter__(self):
        return iter(self._symlink_paths)

    def __contains__(self, value):
        return value in self._symlink_paths

    def __len__(self):
        return len(self._symlink_paths)
