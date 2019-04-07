from pysymreplace import SymlinkFinderService


def test_symlink_finder_finds_single_symlink(tmp_path):
    symlink = tmp_path / 'symlink'
    symlink.symlink_to('target')

    finder = SymlinkFinderService()
    symlink_paths = finder.find_symlinks([tmp_path])

    assert len(symlink_paths) == 1
    assert symlink_paths == set([str(symlink)])

def test_symlink_finder_finds_direct_path_to_symlink(tmp_path):
    symlink = tmp_path / 'symlink'
    symlink.symlink_to('target')

    finder = SymlinkFinderService()
    symlink_paths = finder.find_symlinks([symlink])

    assert len(symlink_paths) == 1
    assert symlink_paths == set([symlink])


def test_symlink_finder_excludes_normal_files(tmp_path):
    test_file = tmp_path / 'normal_file'
    test_file.touch()

    finder = SymlinkFinderService()
    symlink_paths = finder.find_symlinks([test_file])

    assert len(symlink_paths) == 0


def test_symlink_finder_finds_multiple_symlinks(tmp_path):
    first_symlink = tmp_path / 'first'
    second_symlink = tmp_path / 'second'

    first_symlink.symlink_to('first_target')
    second_symlink.symlink_to('second_target')

    finder = SymlinkFinderService()
    symlink_paths = finder.find_symlinks([tmp_path])

    assert len(symlink_paths) == 2
    assert symlink_paths == set([str(first_symlink), str(second_symlink)])
