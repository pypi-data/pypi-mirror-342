# Constafor Packages

This is a simple example package. You can use
[GitHub-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

### Initialize
```sh
pip install -e .
```

### Manual upload to GitHub
```sh
python -m twine upload --repository-url https://api.github.com/orgs/Constrafor/packages/pypi/upload sample_package/dist/*
```
