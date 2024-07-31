# %%
                        #---Inheritance in Python---
#parent class --> base class
#child class --> derived class

#Parent class
class Person:
    def __init__(self, fname, lname) -> None:
        self.firstname = fname
        self.lastname = lname

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"
    

class Student(Person):
    def __init__(self, fname, lname, gradyear) -> None:
        super().__init__(fname, lname)
        self.gradyear = gradyear
    
    def welcome(self):
        print(f"Welcome {self.firstname} {self.lastname} to the class of {self.gradyear}")
    
p1 = Student("Hafsa","Manan",2024)
print(p1) # uses the str method in the parent class
p1.welcome() #use the welcome method in the child class(student)

#%%
                        #---polymorphism in Python
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Drive!")

class Boat:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Sail!")

c1 = Car("Ford", "mustang")

b1 = Boat("White Star Line", "Titanic")

for x in (c1,b1):
    x.move()


# %%
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Drive!")

class Boat:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Sail!")

c1 = Car("Ford", "mustang")

b1 = Boat("White Star Line", "Titanic")

for x in (c1,b1):
    x.move()

#%%
#Method overridding

class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Vroom!")

class Car(Vehicle):
    pass

class Boat(Vehicle):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Sail!")

c1 = Car("Ford", "mustang")

b1 = Boat("White Star Line", "Titanic")
for x in (c1,b1):
    x.move()


