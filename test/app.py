class model(dict):
    def __init__(self,*arg):
        super().__init__(*arg)
    def save(self, val):
        print(self)
        self.update(val)
        print(self)

obj = model({"dddsd":"dsdadadada"})
obj.save({"dsda":"dsda"})