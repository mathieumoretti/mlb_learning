class Category:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        return 'Category does not have `{}` attribute.'.format(str(name))
