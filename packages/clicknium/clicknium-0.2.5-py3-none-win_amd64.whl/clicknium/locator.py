class _Locator:
    def __init__(self, path=None):
        self._path = path

    def __getattr__(self, path):
        if self._path:
            new_path = self._path + "." + path
        else:
            new_path = path

        return _Locator(new_path)

    def __str__(self):
        return self._path