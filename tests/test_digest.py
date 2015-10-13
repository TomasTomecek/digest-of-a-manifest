import os

from digest import *


def test_decode_manifest():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(this_dir, "./manifest.json")
    expected_manifest_path = os.path.join(this_dir, "./expected-manifest.json")
    manifest = open(manifest_path, "r").read()
    expected_manifest = open(expected_manifest_path, "r").read()
    result = prepare_file_decode(manifest)
    for idx, v in enumerate(expected_manifest):
        if not v == result[idx]:
            # char by char debugging
            print "-", repr(expected_manifest[idx-15:idx+45])
            print "-", repr(result[idx-15:idx+45])
            break
    assert result == expected_manifest


def test_hack_manifest():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(this_dir, "./manifest.json")
    expected_manifest_path = os.path.join(this_dir, "./expected-manifest.json")
    manifest = open(manifest_path, "r").read()
    expected_manifest = open(expected_manifest_path, "r")
    result = prepare_file_hack(manifest)
    assert result == expected_manifest.read()


def test_digest():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    expected_manifest_path = os.path.join(this_dir, "./expected-manifest.json")
    with open(expected_manifest_path, "r") as fd:
        expected_manifest = fd.read()
    digest = compute_digest(expected_manifest)
    expected_digest = "sha256:3bd99e8c083e6bb60ef9c1e7de1a2c34a1fab103b6ee4e9c23f08abd91fb6d53"
    assert digest == expected_digest
