

class Player:
    def __init__(self, *args, **kwargs):
        if len(args) < 1:
            self.ctr_0()
        elif len(args) < 2:
            self.ctr_1(args[0])
        elif len(args) < 3:
            self.ctr_2(args[0], args[1])
        else:
            raise ValueError
        return super().__init__()

    def ctr_0(self):
        self.name = ""
        self.espn_id = -1

    def ctr_1(self, name):
        self.ctr_0()
        self.name = name

    def ctr_2(self, name, espn_id):
        self.ctr_1(name)
        self.espn_id = espn_id

    def __setattr__(self, name, value):        
        self.__dict__[name] = value

    def __getattr__(self, name):
        return 'Player does not have `{}` attribute.'.format(str(name))