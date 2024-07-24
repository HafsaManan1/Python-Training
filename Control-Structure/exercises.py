                        #---if else statements---
#%%
a = 200
b = 33
if a > b: print("a is greater than b")
#%%
x=4
y=3
print("x is greater than y")if x>y else print("y is greater than x")
#%%
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")
#%%
#program to give grade based on percentage entered by user
x = int(input("Enter the percentage:"))
if x>90:
  print("Grade A")
elif x>80 and x<=90:
  print("Grade B")
elif x>=60 and x<=80:
  print("Grade C")
else:
  print("Grade D")
#%%
#code to check whether a year is leap or not
x=int(input("Please enter a year"))
if (x % 4 == 0 and x % 100 != 0) or (x % 400 == 0):
    print(x,"is a leap year")
else:
  print("year is not leap")
#%%
#code to check if a number is divisible by both 2 and three
x=int(input("Please enter a year"))
if x%2==0 and x%3==0:
  print("The number is divisible by both 2 and 3")
else:
  print("The number is not divisible by 2 and 3")
#%%
#Ternary operators
x=int(input("Please enter a year"))
print("x is postive") if x>0 else print("x is negative") 
#%%
#check if a list is empty or not
x=[]
if x:
  print("list is not empty")
else:
  print("list is empty")
#%%
#string comparison
str="hello"
x=input("Enter a string")
x=x.lower()
if x==str:
  print("The text matches")
#%%
                        #---while loops---
i=1
while i<6:
  print(i)
  i+=1

# %%
#Write a program that asks the user to enter a number. 
# Use a while loop to keep asking until the user enters a number greater than 10.
while True:
  x=int(input("Enter a Number"))
  if x>=10:
    break
  
# %%
#Write a program that calculates the sum of all even numbers from 1 to 20 using a while loop.
i=1
sum=0
while i<=20:
  sum=sum+i
  i+=1
print("sum is:",sum)
  
# %%
#code to count number of digits in a number
x=23473737
numbers=0
while x:
  numbers+=1
  x=x//10
print(numbers)
  

# %%
                        #---for loop---
"""
1 
1 2 
1 2 3 
1 2 3 4 
1 2 3 4 5"""
row = 5
for i in range(1,6):
  for j in range(1,i+1):
    print(j,end="")
  print("\n")
# %%
#looping in list
l = [1,2,3,4]
for i in l:
  print(i)

# %%
#looping in tuples
t = (2,3,5,9)
for i in t:
  print(i)

# %%
#looping in sets
s = {2,9,8,1,3}
for i in s:
  print(i)
print(s)
# %%
#In the loop, when the item value is "banana", jump directly to the next item.
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
  if fruit=="banana":
    continue
  print(fruit)

# %%
#Exit the loop when x is "banana"
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
  if fruit=="banana":
    break
  print(fruit)