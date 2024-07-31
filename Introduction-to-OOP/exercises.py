                        #--- Classes in Python
#%%
#creating a simple class and an object
class MyClass:
    x=5

p1 = MyClass()
print(p1.x)
# %%
#using the init function
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
p1 = Person("John",22)
print(p1.name)
print(p1.age)

# %%
#printing instance without the __str__ function
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
p1 = Person("John",22)
print(p1)
# %%
#print with the __str__ function

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name} {self.age} "
    
    def greeting(self):
        print(f"Hello my name is {self.name} and I am {self.age} years old.")
    
p1 = Person("John",22)
p1.greeting()
# %%
#self is just a naming convention. We can use anything in the place of self.
class Person:
  def __init__(mysillyobject, name, age):
    mysillyobject.name = name
    mysillyobject.age = age

  def myfunc(abc):
    print("Hello my name is " + abc.name)

p1 = Person("John", 36)
p1.myfunc()
# %%
#modifying the properties of objects

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name} {self.age} "
    
    def greeting(self):
        print(f"Hello my name is {self.name} and I am {self.age} years old.")
    
p1 = Person("John",22)
p1.age = 54
del p1.age # can delete the property of the object by del keyword
del p1 # to delete the whole object
p1.greeting()
#%%
#class attributes
class Items:
    sale = 0.5
    def __init__(self,name:str, price:float):
        self.name = name
        self.price = price

i = Items("Mobile",234)
print(i.sale)
print(Items.sale)

#%%
#instance attributes

class Items:
    sale = 0.5
    def __init__(self,name:str, price:float):
        self.name = name
        self.price = price

i1 = Items("Mobile",234)
i2 = Items("Laptop",767)
i2.sale=0.7 # changing the value for a specific instance of the class
print(i1.sale)
print(i2.sale) # now look for the value on the instance level first
print(Items.sale)

# %%
                        #---iterator---
#iterators in list
mylist = ['apples','bananas','strawberries','apricot']

myitr = iter(mylist)

#print(myitr.__next__())
print(next(myitr))
print(next(myitr))
print(next(myitr))
print(next(myitr))
# %%
#iterators in strings
mystr = "banana"
myitr = iter(mystr)
print(next(myitr))
print(next(myitr))
print(next(myitr))
print(next(myitr))
print(next(myitr))
print(next(myitr))
# %%
class Mynumber:
    def __init__(self):
        self.a = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.a <=20:
            x = self.a 
            self.a+=1
            return x
        else: 
            raise StopIteration
myclass = Mynumber()
#myitr = iter(myclass)

print(next(myclass))

for x in myclass:
    print(x)

# %%
                        #---Decorators in Python---

def mydecorator(function):
    def wrapper(*args,**kwargs):
        print("*I am decorating your function*")
        return function(*args,**kwargs)
    return wrapper
    
@mydecorator
def hello(name):
    return (f"Hello {name}!!")
print(hello("Hafsa"))

# %%
