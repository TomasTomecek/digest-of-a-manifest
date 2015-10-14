import os
import sys
from cStringIO import StringIO

from digest import *

import pytest


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
EXPECTED_DIGEST = "sha256:3bd99e8c083e6bb60ef9c1e7de1a2c34a1fab103b6ee4e9c23f08abd91fb6d53"
MOCK_VAL = "asd"


@pytest.fixture
def manifest():
    manifest_path = os.path.join(THIS_DIR, "./manifest.json")
    with open(manifest_path, "r") as fd:
        return fd.read()


@pytest.fixture
def expected_manifest():
    expected_manifest_path = os.path.join(THIS_DIR, "./expected-manifest.json")
    with open(expected_manifest_path, "r") as fd:
        return fd.read()


def test_decode_manifest(manifest, expected_manifest):
    m = Manifest(manifest)
    result = m.render(m.prepare_for_digest_computation())
    for idx, v in enumerate(expected_manifest):
        if not v == result[idx]:
            # char by char debugging
            print "-", repr(expected_manifest[idx-15:idx+45])
            print "-", repr(result[idx-15:idx+45])
            break
    assert result == expected_manifest


def test_hack_manifest(manifest, expected_manifest):
    result = prepare_file_hack(manifest)
    assert result == expected_manifest


def test_digest(manifest):
    m = Manifest(manifest)
    digest = m.digest
    assert digest == EXPECTED_DIGEST


def test_set_name(manifest):
    m = Manifest(manifest)
    m.set_name(MOCK_VAL)
    assert m.decoded_manifest["name"] == MOCK_VAL


def test_set_tag(manifest):
    m = Manifest(manifest)
    m.set_tag(MOCK_VAL)
    assert m.decoded_manifest["tag"] == MOCK_VAL


def test_cli():
    manifest_path = os.path.join(THIS_DIR, "./manifest.json")
    sys.argv = ["digest.py", manifest_path]
    stdout = sys.stdout
    sys.stdout = StringIO()
    with pytest.raises(SystemExit):
        main()
    result = sys.stdout.getvalue().strip()
    sys.stdout = stdout
    assert result == EXPECTED_DIGEST
