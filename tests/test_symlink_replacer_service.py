import pytest
from pysymreplace import SameRelativePathsError, SymlinkReplacerService


def test_symlink_replacer_replaces_symlink(tmp_path):
    target = tmp_path / 'target'
    target.touch()

    symlink = tmp_path / 'symlink'
    symlink.symlink_to(target)

    assert symlink.is_symlink()

    replacer = SymlinkReplacerService()
    replacer.replace_symlink_with_target(symlink)

    assert not target.exists()
    assert symlink.exists() and not symlink.is_symlink()


def test_symlink_replacer_replaces_parent_and_child(tmp_path):
    directory = tmp_path / 'directory'
    directory.mkdir()

    parent_symlink = tmp_path / 'parent'
    parent_symlink.symlink_to(directory)

    target = parent_symlink / 'target'
    target.touch()

    child_symlink = parent_symlink / 'child'
    child_symlink.symlink_to(target)

    replacer = SymlinkReplacerService()
    replacer.replace_symlinks_with_target([parent_symlink, child_symlink])

    assert not directory.exists()
    assert not target.exists()
    assert parent_symlink.exists() and not parent_symlink.is_symlink()
    assert (parent_symlink / 'child').exists()


def test_symlink_replacer_replaces_cross_symlinks(tmp_path):
    directory = tmp_path / 'directory'
    directory.mkdir()

    parent_symlink = tmp_path / 'parent'
    parent_symlink.symlink_to(directory)

    target = directory / 'target'
    target.touch()

    child_symlink = parent_symlink / 'child'
    child_symlink.symlink_to(target)

    replacer = SymlinkReplacerService()
    replacer.replace_symlinks_with_target([parent_symlink, child_symlink])

    assert not directory.exists()
    assert not target.exists()
    assert parent_symlink.exists() and not parent_symlink.is_symlink()
    assert (parent_symlink / 'child').exists()


def test_symlink_replacer_errors_given_same_references(tmp_path):
    target = tmp_path / 'target'
    target.touch()

    first_symlink = tmp_path / 'first'
    first_symlink.symlink_to(target)

    second_symlink = tmp_path / 'second'
    second_symlink.symlink_to(target)

    replacer = SymlinkReplacerService()

    with pytest.raises(SameRelativePathsError):
        replacer.replace_symlinks_with_target([first_symlink, second_symlink])


def test_symlink_replacer_errors_given_invalid_symlink(tmp_path):
    symlink = tmp_path / 'symlink'
    symlink.symlink_to('invalid_target')

    replacer = SymlinkReplacerService()

    with pytest.raises(FileNotFoundError):
        replacer.replace_symlink_with_target(symlink)


def test_symlink_replacer_errors_given_link_loop(tmp_path):
    symlink = tmp_path / 'symlink'
    symlink.symlink_to(symlink)

    replacer = SymlinkReplacerService()

    with pytest.raises(RuntimeError) as exc:
        replacer.replace_symlink_with_target(symlink)

    assert exc.match('Symlink loop')
