class Position:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        return 'Category does not have `{}` attribute.'.format(str(name))

    def __eq__(self, other):            
        if isinstance(other, Position):
            return self.name == other.name
        return False