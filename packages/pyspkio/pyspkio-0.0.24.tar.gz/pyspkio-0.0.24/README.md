# pyspkio

to build

```console
. env/bin/activate
pip install -r requirements.txt
python3 -m build
```

to upload

```console
python3 -m twine upload --repository pypi dist/*
```


ref:

[Packaging project](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
