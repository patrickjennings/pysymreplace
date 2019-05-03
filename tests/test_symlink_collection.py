from pysymreplace import SymlinkCollection


def test_symlink_collection_finds_symlink(tmp_path):
    symlink = tmp_path / 'symlink'
    symlink.symlink_to('target')

    symlinks = SymlinkCollection(tmp_path)

    assert symlinks == set([symlink])


def test_symlink_collection_finds_symlinks_from_many_paths(tmp_path):
    directory_one = tmp_path / 'directory_one'
    directory_one.mkdir()

    directory_two = tmp_path / 'directory_two'
    directory_two.mkdir()

    symlink_one = directory_one / 'symlink'
    symlink_one.symlink_to('target')

    symlink_two = directory_two / 'symlink'
    symlink_two.symlink_to('target')

    symlinks = SymlinkCollection(directory_one, directory_two)

    assert symlinks == set([symlink_one, symlink_two])
