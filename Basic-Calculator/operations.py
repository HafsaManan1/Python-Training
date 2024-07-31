def number_input():
    num1=float(input("\nEnter 1st number: "))
    num2=float(input("Enter 2nd number: "))
    return num1,num2
    
def addition():
    num1,num2 = number_input()
    return f"\nResult: {num1}+{num2} = {num1+num2}\n"

def subtraction():
    num1,num2 = number_input()
    return f"\nResult: {num1}-{num2} = {num1-num2}\n"

def multiplication():
    num1,num2 = number_input()
    return f"\nResult: {num1}x{num2} = {num1*num2}\n"

def division():
    num1,num2 = number_input()
    if num2==0:
        return ("\nDivision by zero is invalid\n")
    else:    
        return f"\nResult: {num1}÷{num2} = {num1/num2}\n"