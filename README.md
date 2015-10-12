Test with:

```
$ PYTHONPATH="$PWD" py.test-2.7 -vv
```

Current issue is that docker encodes everything as utf-8, except for `<`, `>` and `&`; while python wants unicode.
