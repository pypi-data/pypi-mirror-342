import os

# main.py
def hello():
    print("OS codes Successfuly installed")


def show_codes():
    file_path = os.path.join(os.path.dirname(__file__), "codes.txt")
    try:
        with open(file_path, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("codes.txt not found.")
