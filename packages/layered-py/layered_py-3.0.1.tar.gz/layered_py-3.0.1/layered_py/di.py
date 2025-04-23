class Container:
    def __init__(self):
        self._providers = {}
        self._singletons = {}

    def register(self, key, provider, *, singleton=False):
        self._providers[key] = {
            "provider": provider,
            "singleton": singleton
        }

    def resolve(self, key):
        if key not in self._providers:
            raise KeyError(f"No provider registered for key: '{key}'")

        entry = self._providers[key]

        if entry["singleton"]:
            if key not in self._singletons:
                self._singletons[key] = entry["provider"]()
                return self._singletons[key]
            else:
                return entry["provider"]()