import json

def search_bar():
    find = input("Enter a company")

    try:
        with open("data.json") as file:
            data = json.load(file)
    except:
        print("no saves yet")

    else:
        try:
            mail = data[find]["email"]
            key = data[find]["password"]
        except KeyError:
            print(f"No saves for {find}")
        else:
            print(f"{mail}, {key}")


search_bar()
