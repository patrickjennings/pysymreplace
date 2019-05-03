from pysymreplace import find_and_replace_symlinks


def test_symlink_find_and_replace_symlinks(tmp_path):
    target = tmp_path / 'target'
    target.touch()

    symlink = tmp_path / 'symlink'
    symlink.symlink_to(target)

    symlinks = find_and_replace_symlinks(tmp_path)

    assert symlinks == set([symlink])
