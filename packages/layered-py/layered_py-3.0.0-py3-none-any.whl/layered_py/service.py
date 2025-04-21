class Service:
    def __init__(self, *args, **kwargs):
        self.__dependencies = kwargs
        self.setup()

    def setup(self):
        pass

    def handle(self):
        raise NotImplementedError()