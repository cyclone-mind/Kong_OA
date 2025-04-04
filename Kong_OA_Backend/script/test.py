class Person():
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def to_dict(self):
        return self.__dict__.items()

alex = Person('Alex',18)
print(alex.to_dict())