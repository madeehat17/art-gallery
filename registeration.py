def is_valid_password(password):
    if len(password)<8:
        return False
    has_upper=has_lower=has_digit=has_special=False
    for char in password:
        if char.isupper():
            has_upper=True
        elif char.islower():
            has_lower=True
        elif char.isdigit():
            has_digit=True
        elif not char.isalnum():
            has_special=True
    return has_upper and has_lower and has_digit and has_special
def register():
    username=input("Create username: ")
    while True:
        password=input("Create a password: ")
        if is_valid_password(password):
            break
        else:
            print("\nInvalid password. Password must be 8 characters long and contain:")
            print("- One uppercase letter")
            print("- One lowercase letter")
            print("- One special character")
    file=open("users.txt","a")
    file.write(username+","+password+"\n")
    file.close()
    print("Registration successful!")
register()