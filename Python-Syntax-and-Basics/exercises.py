#%%    
                        #---Python Numbers---
x = 1   
y = 2.8 
z = 1j 
print(type(x))
print(type(y))
print(type(z))
#casting
print(int(2.8))
print(float("3"))
print(str(3.0))
#%%
                        #---Python Strings---
#slicing
b = "Hello, World!"
print(b[2:5])
print(b[:5])
print(b[2:])
print(b[-5:-2])
#modifying stringe
a = "Hello, World!"
print(a.upper())
print(a.lower())
print(a.strip())
print(a.replace("H", "J"))
print(a.split(","))
#String Concatenation
a = "Hello"
b = "World"
c = a + b
print(c)
a = "Hello"
b = "World"
c = a + " " + b
print(c)
#string format
age = 36
txt = f"My name is John, I am {age}"
print(txt)
price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)
txt = f"The price is {20 * 59} dollars"
print(txt)
#Escape Characters
txt = "We are the so-called \"Vikings\" from the north."
print(txt)
#%%
                        #---Python booleans---
print(10 > 9)
print(10 == 9)
print(10 < 9)
print(bool("abc"))
print(bool(123))
print(bool(["apple", "cherry", "banana"]))
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})
#%%
                        #---lists---
thislist = ["apple", "banana", "cherry", "apple", "cherry"]
print(thislist)
print(len(thislist))
print(type(thislist))
thislist = list(("apple", "banana", "cherry","grapes","apricot","mangoes"))
#slicing in lists
print(thislist)
print(thislist[1])
print(thislist[2:5])
print(thislist[:4])
print(thislist[2:])
print(thislist[-4:-1])
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")
#changing list items
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist)
thislist[2:4] = ["watermelon"]
print(thislist)
#insertion in lists
thislist.insert(2,"kiwi")
print(thislist)
thislist.append("orange")
print(thislist)
tropical = ["pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)
thistuple = ("melon","guava")
thislist.extend(thistuple)
print(thislist)
#removing elements in lists
del thislist[10:20]
print(thislist)
thislist.remove("apple")
thislist.pop()
thislist.pop(0)
print(thislist)
thislist.clear()
print(thislist)
#sorting lists
thislist = list(("apple", "banana", "cherry","grapes","apricot","mangoes"))
thislist.sort()
print(thislist)
thislist.sort(reverse=True)
print(thislist)
#customize sort function
def myfunc(n):
  return abs(n - 50)
thislist = [100, 50, 65, 82, 23]
thislist.sort(key = myfunc)
print(thislist)
#case sensitive sort
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort()
print(thislist)
#case insensitive sort
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort(key = str.lower)
print(thislist)
#reversing a string
thislist.reverse()
print(thislist)
#coping a list
thislist = [1,2,3,4,5]
mylist = thislist.copy()
thislist.append(6)
print(thislist)
print(mylist)
#joining lists
print(thislist+mylist)
thislist.extend(mylist)
print(thislist)
#Use a range of indexes to print the third, fourth, and fifth item in the list.
fruits = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(fruits[2:5])
#%%
                        #---Tuples---
mytuple=(1,2,3,4)
print(mytuple)
#changing items in tuples by converting them into list and then again converting them into tuples
new_tuple = list(mytuple)
new_tuple[1]=5
mytuple = tuple(new_tuple)
print(mytuple)
#adding two tuples
mytuple=(1,2,3,4)
new_tuple=(5,)
mytuple +=new_tuple
print(mytuple)
#unpacking a tuple
fruits = ("apple", "banana", "cherry")

(green, yellow, red) = fruits

print(green)
print(yellow)
print(red)
#using * for multiple values
fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")

(green, yellow, *red) = fruits

print(green)
print(yellow)
print(red)
fruits = ("apple", "mango", "papaya", "pineapple", "cherry")

(green, *tropic, red) = fruits

print(green)
print(tropic)
print(red)
#multiplying tuples
fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2

print(mytuple)
#count in tuples
print(mytuple.count("apple"))
#%%
                        #---Sets in python---
myset = {"apple","banana","cherry","apricot"}
print(myset)
#True and 1 are considered as one
thisset = {"apple", "banana", "cherry", True, 1, 2}
print(thisset)
print(len(thisset))
#False and 0 are considered as one
thisset = {"apple", "banana", "cherry", False, 0, 2}
print(thisset)
print(len(thisset))
#accessing items in sets by looping through them
myset = {"apple","banana","cherry","apricot"}
for item in myset:
  print(item)
print("banana" in myset)
print("mangoes" in myset)
#adding items in sets
thisset = {"apple", "banana", "cherry"}
thisset.add("mangoes")
print(thisset)
#combining two sets
thisset = {"apple", "banana", "cherry","mango"}
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)

print(thisset)

#adding a list to a set
thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange","cherry"]

thisset.update(mylist)

print(thisset)

#removing items in sets
thisset = {"apple", "banana", "cherry","kiwi", "orange"}
thisset.remove("banana")
thisset.discard("cherry")
thisset.pop()
print(thisset)
thisset.clear()
print(thisset)
del thisset

#join sets
#union and intersection
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
set4 = set1.intersection(set2)
print(set3)
print(set4)
#joining sets
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1 | set2
print(set3)

#joing set and tuples
x = {"a", "b", "c"}
y = (1, 2, 3)

z = x.union(y)
print(z)
#%%
                        #---Dictionaries---
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict["brand"])

#dict() constructor
thisdict = dict(name = "John", age = 36, country = "Norway")
print(thisdict)

#accessing values in dictionaries
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
x = thisdict["model"]
print(x)

#accessing values using get
thisdict.get("brand")
#accessing keys in dictionaries
x=thisdict.keys()
print(x)
#accessing values in dictionaries
x=thisdict.values()
print(x)
#adding in dictionaries
car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}

x = car.keys()

print(x) #before the change

car["color"] = "white"

print(x) #after the change

#getting items in dictionary
x = thisdict.items()
print(x)

#changing items in dictionaries
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict["year"] = 2018
x=thisdict.items()
print(x)

#changing items in dictionaries using update

thisdict.update({"year":2020})
x=thisdict.items()
print(x)

#removing items
thisdict.pop("brand")
print(thisdict)

thisdict.popitem()
print(thisdict)

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
del thisdict["model"]
print(thisdict)

thisdict.clear()
print(thisdict)
del thisdict
print(thisdict)

#coping dictionaries
dic1= {
    "Book":"All the places I've cried in the public",
    "author":"Holy Born", 
    "year":2020
    }
print(dic1)
copydic = dic1.copy()
print(copydic)
