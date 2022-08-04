
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, name, discount):
        self._name = str(name)

    def __str__(self):
        return "Name: " + self._name

class Manager(User):
    pass


class Employee(User):
    pass

class Customer(User):
    pass
