class Gamelog:
    def __init__(self, *args, **kwargs):
        if len(args) < 1:
            self.ctr_0()
        elif len(args) < 2:
            self.ctr_1(args[0])
        elif len(args) < 3:
            self.ctr_2(args[0], args[1])
        elif len(args) < 4:
            self.ctr_3(args[0], args[1], args[2])
        elif len(args) < 5:
            self.ctr_4(args[0], args[1], args[2], args[3])
        else:
            raise ValueError
        return super().__init__()

    def ctr_0(self):
        self.date = ""
        self.position = ""
        self.player = ""
        self.statline = ""

    def ctr_1(self, date):
        self.ctr_0()
        self.date = date

    def ctr_2(self, date, position):
        self.ctr_1(date)
        self.position = position

    def ctr_3(self, date, position, player):
        self.ctr_2(date, position)
        self.player = player

    def ctr_4(self, date, position, player, statline):
        self.ctr_3(date, position, player)
        self.statline = statline

    def __setattr__(self, name, value):        
        self.__dict__[name] = value
