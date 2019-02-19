from folder1.class1 import Class1

class Class2:
    def __init__(self, *args, **kwargs):
        self.x = "Bro"
        self.y = "Bro"
        return super().__init__(*args, **kwargs)