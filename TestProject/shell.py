import sys

while True:
    try:
        exec(input("8=> "))
    except:
        print(sys.exc_info())
