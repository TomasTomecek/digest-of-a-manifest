#!/usr/bin/python2

"""
This script takes at least one argument: path to a file with manifest.
It then computes and prints digest of the manifest(s).
The main reason this is not done properly, by decoding json, removing `signatures` and
encoding again, is that docker messes up encoding of strings and makes it impossible
to do right. For more info see:
    https://github.com/docker/distribution/issues/1065
"""

import os
import re
import sys
import json
import hashlib

from collections import OrderedDict


def prepare_file_hack(fd):
    """
    prepare manifest for generating digest
    fd: file object returned by open
    """
    # 0 start -> signatures
    # 1 signatures
    # 2 after signatures
    states = 0
    sig_re = r'(\s+)\"signatures\":\s*\['
    stop = None

    ls = []

    for line in fd.readlines():
        if line == stop:
            states = 2
        if states == 1:
            continue
        m = re.match(sig_re, line)
        if m is not None:
            states = 1
            ls = ls[:-1]
            stop = m.groups()[0] + "]\n"
            continue
        else:
            ls.append(line)
    return "".join(ls)


def prepare_file_decode(fd):
    """
    prepare manifest for generating digest
    fd: file object returned by open
    """
    j = fd.read()
    decoded_json = json.loads(j, object_pairs_hook=OrderedDict, encoding="utf-8")
    del decoded_json["signatures"]
    for h in decoded_json["history"]:
        print json.loads(h["v1Compatibility"], object_pairs_hook=OrderedDict, encoding="utf-8")

    # TODO: get rid of all \uXXXX here and make everything utf-8

    encoded_json = json.dumps(decoded_json, indent=3, separators=(',', ': '), ensure_ascii=True)

    # TODO: save it as utf-8, but before that substitue all < > &
    return unicode(encoded_json).encode("utf-8")


def compute_digest(manifest):
    """
    manifest: str
    """
    return hashlib.sha256(manifest).hexdigest()


def main():
    if len(sys.argv[1:]) <= 0:
        print "Provide please at least one path to a file with manifest."
        sys.exit(1)
    result = []
    for fp in sys.argv[1:]:
        p = os.path.abspath(os.path.expanduser(fp))
        with open(p, "r") as fd:
            content = prepare_file(fd)
            digest = compute_digest(content)
            result.append((fp, digest))
    if len(result) == 1:
        print result[0][1]
    else:
        for r in result:
            print "{} {}".format(*r)
    sys.exit(0)


if __name__ == "__main__":
    main()
