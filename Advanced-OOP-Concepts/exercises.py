#%%
                        #---Encapsulation---

#Protected Members
class Base:
    def __init__(self):
        #protected member
        self._a = 10
    
class Derived(Base):
    def __init__(self):
        super().__init__()
        #calling protected member 
        print(f"Calling protected variable of the base class {self._a}")
        #changing value of the protected variable
        self._a = 20
        print(f"After modification of the protected variable {self._a}")
        
b1 = Base()
d1 = Derived()
print(b1._a)
print(d1._a)

# %%
#Privated Members
class Base:
    def __init__(self):
        #protected member
        self.__a = 10
    
    def printing(self):
        print(self.__a)
class Derived(Base):
    def __init__(self):
        super().__init__()
        #calling protected member will raise an error
        #print(f"Calling protected variable of the base class {self.__a}")
        #changing value of the protected variable will raise an error
        #self.__a = 20
        #print(f"After modification of the protected variable {self.__a}")
        
b1 = Base()
# d1 = Derived()
#print(b1.__a) cannot access the private member outside

# %%
                        #---Class Methods---
import csv
class Items:
    sale = 0.5
    all = []
    def __init__(self,name:str, price:float):
        self.name = name
        self.price = price
        Items.all.append(self)

    def __repr__(self): # for returning the instance in the same format it was created in
        return f"Items('{self.__class__.__name__}{self.name}',{self.price})"

    def __str__(self): # for making the output pretty
        return f"Product: {self.name} Price: {self.price}"
    # str has precedence over repr
    @classmethod
    def loading_from_csv(cls):
        with open('items.csv','r') as f:
            reader = csv.DictReader(f)
            items = list(reader)
            print(items)

        for item in items:
            Items(
                name=str(item.get('name')),
                price=int(item.get('price'))
            )
Items.loading_from_csv()
print(Items.all)

#%%
                        #---Static Methods---
class Dummy:
    def __init__(self):
        pass

    @staticmethod #they donot need self parameter and they can be called without creating an object of the class i.e,. straight from the class itself.
    def is_integer(num):
        if isinstance(num,int):
            print(True)
        else:
            print(False)
        
Dummy.is_integer(8)
d1 = Dummy()
d1.is_integer(9.9)
#%%
#property, getter, setter

class Items:
    def __init__(self,name,price):
        self.__name = name
        self.price = price

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,value):
        self.__name = value

    


i1 = Items("Phone",7000)
print(i1.name)
i1.name = "Laptop"
print(i1.name)
# %%
                        #---Abstraction---
#abstract classes and methods


from abc import ABC, abstractmethod

class Car(ABC):

    @classmethod
    def mileage(self): #abstact method has declaration but no implementation
        pass

class Suzuki(Car):
     
    def mileage(self):
        print("The mileage is 25kmph")

class Tesla(Car):

    def mileage(self):
        print("The mileage is 30kmph")

t = Tesla()
t.mileage()
s= Suzuki()
s.mileage()

# %%
                        #---Composition---
class Salary:
    def __init__(self,pay,bonus):
        self.pay = pay
        self.bonus = bonus

    def annual_salary(self):
        return (self.pay*12 + self.bonus)
    

class Employee:
    def __init__(self,name,age,pay,bonus):
        self.name = name
        self.age = age
        self.obj_salary = Salary(pay,bonus)

    def yearly_salary(self):
        return self.obj_salary.annual_salary()
    
e1 = Employee('Hamza',22,100000,12000)
print(e1.yearly_salary())
        
# %%
