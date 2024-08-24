# BLUEPRINT | DONT EDIT
while True:
    try:
        a = int(input("Choose a number:\n"))
        b = int(input("Choose another one:\n"))
    except ValueError:
        print("Invalid number. Numbers only")
        continue

    operation = input(
        "Choose an operation:\n    Options are: + , - , * or /.\n    Write 'exit' to finish.\n"
    )
    # /BLUEPRINT

    # 👇🏻 YOUR CODE 👇🏻:

    if operation.lower() == "exit":
        break

    result: float

    if operation == "+":
        result = a + b
    elif operation == "-":
        result = a - b
    elif operation == "*":
        result = a * b
    elif operation == "/":
        if b == 0:
            print("Cannot divide by zero")
            continue
        else:
            result = a / b
    else:
        print("You should type operator or 'exit'")
        continue

    print("Result: {0}".format(result))

# /YOUR CODE
