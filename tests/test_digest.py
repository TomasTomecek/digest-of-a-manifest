import os

from digest import prepare_file_decode


def test():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(this_dir, "./manifest.json")
    expected_manifest_path = os.path.join(this_dir, "./expected-manifest.json")
    manifest = open(manifest_path, "r")
    expected_manifest = open(expected_manifest_path, "r")
    result = prepare_file_decode(manifest)
    assert result == expected_manifest.read()
