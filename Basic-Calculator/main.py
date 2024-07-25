from operations import addition, subtraction, multiplication, division
opt=0
while opt!=5:
    print("""\nOPTIONS:
        1-ADDITION
        2-SUBTRACTION
        3-MULTIPLICATION
        4-DIVISION
        5-EXIT\n""")
    
    opt=int(input("Select an operation by entering a number: "))

    if opt==1:
        print(addition())
    elif opt==2:
        print(subtraction())
    elif opt==3:
        print(multiplication())
    elif opt==4:
        print(division())
    elif opt==5:
        print("\nSuccessfully Exited!")
        break
    else:
        print("Invalid Option, Please select an option again")


