class WrappedResp:
    def __init__(self, value):
        self._value = value

    def json(self):
        return {'results': self._value}
