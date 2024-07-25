#%%
                        #---Functions---
#Python function to find the maximum of three numbers
def max_of_three(x,y,z):
    if x>y and x>z:
        return x
    elif y>x and y>z:
        return y
    else:
        return z
print(max_of_three(10,20,30))
#%%
#Python function to sum all the numbers in a list
def sum_of_list(list):
    sum=0
    for i in list:
        sum+=i
    return sum
print(sum_of_list([1,2,3,4]))
#%%
#function to multiply all the numbers in a list
def multiply_of_list(list):
    mul=1
    for i in list:
        mul*=i
    return mul
print(multiply_of_list([1,2,3]))
#%%
#program to reverse a string
def revserse_string(str):
    for s in range(len(str)):
        print(str[-1],end="")
        str = str[0:len(str)-1]
revserse_string("abc")
#%%
#function to calculate the factorial of a number
def factorial(x):
    fact=1
    for i in range(1,x+1):
        fact*=i
    return fact
print(factorial(12))
#%%
#function that accepts a string and counts the number of upper and lower case letters
def count_upper_lower(str):
    upper=0
    lower=0
    for s in str:
        if s.isupper():
            upper+=1
        elif s.islower():
            lower+=1
        else:
            pass
    return f"Upper case characters = {upper} \nLower case charactors = {lower}"
print(count_upper_lower("A Brown Fox"))
#%%
#function that takes a list and returns a new list with distinct elements from the first list.
def distinct_list(list):
    new_list=[]
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list
print(distinct_list([1,2,3,3,3,3,4,5]))
#%%
#function that takes a number as a parameter and checks whether the number is prime or not
def is_prime(num):
    if num==1:
        return f"{num} is neither prime nor composite"
    for i in range(2,num//2):
        if num%i==0:
            return f"{num} is not prime"
            break
        else:
            return f"{num} is a prime number"

print(is_prime(41))
#%%
#function that checks whether a passed string is a palindrome or not
def is_palindrome(str):
    start = 0
    end = len(str)-1
    while start<end:
        if str[start] != str[end]:
            return "Not a palindrome"
        start+=1
        end-=1
        return True
print(is_palindrome("Hafsa"))
#%%
                        #---Recursion---
#recursive function to calculate the sum of n natural numbers
def sum_with_recursion(n):
    if n==1:
        return 1
    return n+sum_with_recursion(n-1)

print(sum_with_recursion(3))
#%%
#power of a number
def power_with_recursion(num,power):
    if power!=0:
        return num*power_with_recursion(num,power-1)
    else:
        return 1
print(power_with_recursion(2,3))
#%%
#factorial using recursion
def factorial_recursion(num):
    if num>1:
        return num*factorial_recursion(num-1)
    else: 
        return 1
print(factorial_recursion(12))
#%%
#reversing a number using recursion
def reverse_recursion(num):
    if num!=0:
        print(num%10,end="")
        return reverse_recursion(num//10)
reverse_recursion(1234)
#%%
#prime number using recursion
def prime_recursion(num,i=2):
    if num%i==0:
        return False
    else:
        return True
    return prime_recursion(num,i+1)

print(prime_recursion(42))
#%%
#largest element in an array
def largest_recursion(A,n):
    if n==0:
        return A[0]
    return max(A[n-1],largest_recursion(A,n-1))
print(largest_recursion([1,2,3,4],4))
#%%
                        #---Lambda---
#usage of lambda function
x=lambda a,b:a+b
print(x(2,3))
#%%
#lambda function in another function
def my_func(n):
    return lambda a: a*n
doubler = my_func(2)
tripler = my_func(2)
print(doubler(2))
print(tripler(3))
#%%
#map function with lambda function
l = [1,2,3,4,5]
squares = list(map(lambda x: x**2,l))
print(squares)

#%%
#filter function with lambda function
l = [1,2,3,4,5]
is_even = filter(lambda x:x%2==0,l)
even_list = list(is_even)
print(even_list)
