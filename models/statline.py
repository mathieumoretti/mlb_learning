from .categories import Categories

categories = Categories.get_categories()
class Statline:
    def __init__(self, statdict):
        self.categories = dict.fromkeys(list(map(lambda x: x.name, categories)))
        self.reset()
        self.fill(statdict)
        return super().__init__()

    def reset(self):
        for category in categories:
            self.categories[category.name] = 0
    
    def fill(self, statdict):
        for key, value in statdict.items():
            self.categories[key] = value
    
    def __getattr__(self, name):
        return 'Statline does not have `{}` attribute.'.format(str(name))