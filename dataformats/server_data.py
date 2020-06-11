class ServerData:
    def __init__(self):
        self._prefixes = ["u!"]

    # サーバープレフィックス
    @property
    def prefixes(self):
        return self._prefixes

    @prefixes.setter
    def prefixes(self, prefs):
        self._prefixes = prefs
