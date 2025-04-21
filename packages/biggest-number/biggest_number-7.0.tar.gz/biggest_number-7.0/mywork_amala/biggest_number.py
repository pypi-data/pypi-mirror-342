def largest_of_three(a,b,c):
    if a>b and a>=c:
        return a
    elif b>=a and b>=c:
        return b
    else:
        returnc
def get_user_input():
    a=float(input("Enter the first number:"))
    b=float(input("Enter the second number:"))
    c=float(input("Enter the third number:"))
    return a,b,c
def main():
    a,b,c=get_user_input()
    largest=largest_of_three(a,b,c)
    print(f"The largest number is:{largest}")
if__name__=="__main__":
    main()