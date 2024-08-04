class ReprMixin:
    def __repr__(self):
        keyvalues = []
        for key, value in self.__dict__.items():
            keyvalues.extend([key, '=', repr(value), ','])
        result = ''.join(keyvalues[0:-1])
        return f'{self.__class__.__name__}({result})'
