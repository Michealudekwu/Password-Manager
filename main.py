from tkinter import *
from tkinter import messagebox
import pyperclip
import json
import os
from cryptography.fernet import Fernet

if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key", "wb") as enc_file:
        enc_file.write(key)

with open("secret.key", "rb") as enc_key:
    key = enc_key.read()

fernet = Fernet(key)

def pass_gen():
    password_gap.delete(0, END)
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    lets = [random.choice(letters) for _ in range(nr_letters)]
    password_list += lets
    symbol = [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += symbol
    nums = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list += nums

    random.shuffle(password_list)

    new_pass = "".join(password_list)
    password_gap.insert(0, new_pass)

    pyperclip.copy(new_pass)

def search_bar():
    find = web_gap.get()

    try:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
        fernet = Fernet(key)

        with open("encrypted_data.json","rb") as encfile:
            enc_data = encfile.read()
        decrypt_data = fernet.decrypt(enc_data)

        data = json.loads(decrypt_data.decode())

    except:
        messagebox.showerror(title="NO SAVES", message="Docs couldn't be reached")

    else:
        try:
            mail = data[find]["email"]
            key = data[find]["password"]
        except KeyError:
            messagebox.showerror(title="INVALID ORG", message=f"No saves for {find}")
        else:
            messagebox.showinfo(title=f"{find}", message=f"EMAIL = {mail} \nPASSWORD = {key}")


def onclick():
    user = email_gap.get()
    pas = password_gap.get()
    website = web_gap.get()

    new_data = {
        website:{
            "email": user,
            "password": pas
        }
    }

    if len(pas) <= 0 or len(website) <=0:
        messagebox.showinfo(title="Oops", message="Please you have left a field empty")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {user} \nPassword: {pas} \n is this okay?")

        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)

            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}
            data.update(new_data)

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

            with open("data.json", "rb") as file:
                original = file.read()
            encrypt = fernet.encrypt(original)

            with open("encrypted_data.json", "wb") as enc_write:
                enc_write.write(encrypt)

    os.remove("data.json")
    clear()

def clear():
    web_gap.delete(0, END)
    password_gap.delete(0, END)

window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")


lock_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100,100, image = lock_img)
canvas.grid(column=1, row=0)

search = Button(text="search", width=15, command=search_bar)
search.grid(column=2, row=1)

web_name = Label(text="Website:")
web_name.grid(column=0, row=1)
web_gap = Entry(width=35)
web_gap.focus()
web_gap.grid(column=1, row=1)

email = Label(text="Email/Username:")
email.grid(column= 0, row=2)
email_gap = Entry(width=35)
email_gap.insert(0, "michealudekwu@gmail.com")
email_gap.grid(column= 1, row=2)

password = Label(text="Password:")
password.grid(column=0, row= 3)
password_gap = Entry(width=26)
password_gap.grid(column=1, row=3)

generate = Button(text="Generate Password", command=pass_gen)
generate.grid(column=2, row=3)

add = Button(text="Add", width=36, command=onclick)
add.grid(column=1, row=4, columnspan=2)

window.mainloop()
