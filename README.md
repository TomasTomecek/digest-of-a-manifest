# `f(manifest) → digest`

[![Circle CI](https://circleci.com/gh/TomasTomecek/digest-of-a-manifest.svg?style=svg)](https://circleci.com/gh/TomasTomecek/digest-of-a-manifest)

This is a simple python script which is able to calculate digest from provided manifest.

Use it like this:

```
$ digest.py path/to/manifest.json
sha256:d7c67635d6bb320b17dbeed8bccc9261f61ab0bd4e81f3ecb34af899ea471ac0
```

Don't you have manifest? You can easily generate one:

```
$ ./generate_manifest.sh
```

This project also has very simple test suite (you should run it from root of the project):

```
$ PYTHONPATH="$PWD" py.test
```

## Resources

 * https://github.com/docker/distribution/issues/1066
 * https://github.com/docker/distribution/issues/1065
 * http://blog.tomecek.net/post/get-digest-of-a-manifest/
