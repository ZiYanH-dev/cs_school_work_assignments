class man:
    def __init__(self):
        self.__name='kobe'
        self.__age=12
        self._dd=34
    def getter(self):
        return self.__age

k=man()
k.__age=1212
print(k.__age)
print(k._man__age)
