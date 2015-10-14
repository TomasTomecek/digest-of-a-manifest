#!/usr/bin/python2

"""
This script takes at least one argument: path to a file with manifest.
It then computes and prints digest of the manifest(s).
"""
from copy import deepcopy

import os
import re
import sys
import json
import hashlib

from collections import OrderedDict


class Manifest(object):
    def __init__(self, manifest):
        """
        :param manifest: str, json-encoded manifest
        """
        self._encoded_manifest = manifest
        self._decoded_manifest = None

    def prepare_for_digest_computation(self):
        """
        strip "signatures" from decoded manifest

        :return: decoded manifest (instance of OrderedDict)
        """
        decoded_manifest = deepcopy(self.decoded_manifest)
        del decoded_manifest["signatures"]
        return decoded_manifest

    @property
    def digest(self):
        """
        E.g.

        sha256:3bd99e8c083e6bb60ef9c1e7de1a2c34a1fab103b6ee4e9c23f08abd91fb6d53
        """
        decoded_manifest = self.prepare_for_digest_computation()
        return "sha256:" + hashlib.sha256(self.render(decoded_manifest)).hexdigest()

    @property
    def decoded_manifest(self):
        if self._decoded_manifest is None:
            self._decoded_manifest = json.loads(
                self._encoded_manifest, object_pairs_hook=OrderedDict, encoding="utf-8")
            # # This is left here just to keep track of past progress
            # for h in decoded_json["history"]:
            #     # print json.loads(h["v1Compatibility"], object_pairs_hook=OrderedDict,
            #                        encoding="utf-8")
            #     i = h["v1Compatibility"]
            #     i = i.replace(r"\u003c", "<").replace(r"\u003e", ">").replace(r"\u0026", "&")
            #     h["v1Compatibility"] = i
            #     # print i
        return self._decoded_manifest

    def set_tag(self, tag):
        """
        :param tag: str
        :return: None
        """
        self.decoded_manifest["tag"] = tag

    def set_name(self, name):
        """
        :param name: str
        :return: None
        """
        self.decoded_manifest["name"] = name

    def render(self, decoded_manifest=None):
        """
        serialize decoded manifest to json

        :returns: str
        """
        decoded_manifest = decoded_manifest or self.decoded_manifest
        encoded_manifest = json.dumps(
            decoded_manifest, indent=3, separators=(',', ': '), ensure_ascii=False)
        # # This is left here just to keep track of past progress
        # encoded_json = encoded_json.replace("<", r"\\u003c").replace(">", r"\\u003e"
        #     ).replace("&", r"\\u0026")
        return encoded_manifest.encode("utf-8")


def prepare_file_hack(manifest):
    """
    This is a hacky implementation which removes 'signatures' using regular expressions,
    for more info see:

        https://github.com/docker/distribution/issues/1065

    :param manifest: str, json-encoded manifest
    """
    # 0 start -> signatures
    # 1 signatures
    # 2 after signatures
    states = 0
    sig_re = r'(\s+)\"signatures\":\s*\['
    stop = None

    ls = []

    for line in manifest.split("\n"):
        if line == stop:
            states = 2
        if states == 1:
            continue
        m = re.match(sig_re, line)
        if m is not None:
            states = 1
            ls = ls[:-1]
            stop = m.groups()[0] + "]"
            continue
        else:
            ls.append(line)
    return "\n".join(ls)


def main():
    if len(sys.argv[1:]) <= 0:
        print "Provide please at least one path to a file with manifest."
        sys.exit(1)
    result = []
    for fp in sys.argv[1:]:
        p = os.path.abspath(os.path.expanduser(fp))
        with open(p, "r") as fd:
            raw_manifest = fd.read()
            m = Manifest(raw_manifest)
            digest = m.digest
            result.append((fp, digest))
    if len(result) == 1:
        print result[0][1]
    else:
        for r in result:
            print "{} {}".format(*r)
    sys.exit(0)


if __name__ == "__main__":
    main()
