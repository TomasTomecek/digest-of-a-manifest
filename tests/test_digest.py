import os

from digest import prepare_file_decode


def test():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(this_dir, "./manifest.json")
    expected_manifest_path = os.path.join(this_dir, "./expected-manifest.json")
    manifest = open(manifest_path, "r")
    expected_manifest = open(expected_manifest_path, "r").read()
    result = prepare_file_decode(manifest)
    for idx, v in enumerate(expected_manifest):
        if not v == result[idx]:
            print repr(expected_manifest[idx-15:idx+45])
            print repr(result[idx-15:idx+45])
            break
    assert result == expected_manifest
