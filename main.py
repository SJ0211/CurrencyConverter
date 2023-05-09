import tkinter as tk
from tkinter import PhotoImage
import requests
import random
from random import randint
import time

# Overall Structure by Lucas
# API code found by Lucas
url = "https://api.apilayer.com/exchangerates_data/convert"
headers = {
    "apikey": "<Your api key>"
}

# Goverment siezes your funds fun ftn, made by Zion, edited by SJ
n = random.randint(1,100)
if n == 1:
    Seize = True
else:
    Seize = False


# Define the GUI
root = tk.Tk()
root.title("Currency Converter")

# Load the background image
bg_image = PhotoImage(file="background.png")

# Create a label for the background image and place it at the back of the root window
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Define the input fields
amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=0, column=0)

amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1)

from_label = tk.Label(root, text="From:")
from_label.grid(row=1, column=0)

currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "HKD", "NZD", "KRW", "BTC"]

# Dropdown menues by SJ/Zion

from_var = tk.StringVar(value=currencies[0])
from_menu = tk.OptionMenu(root, from_var, *currencies)
from_menu.grid(row=1, column=1)

to_label = tk.Label(root, text="To:")
to_label.grid(row=2, column=0)

to_var = tk.StringVar(value=currencies[1])
to_menu = tk.OptionMenu(root, to_var, *currencies)
to_menu.grid(row=2, column=1)

# tax and seized labels by SJ
tax_label = tk.Label(root, text="")
tax_label.grid(row=3, column=0, columnspan=2)

seized_label = tk.Label(root, text="")
seized_label.grid(row=3, column=0, columnspan=2)

result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

# Define the text box to display messages
#message_box = tk.Text(root, height=3, width=50)
#message_box.grid(row=4, column=0, columnspan=2)

# Conversion function by Lucas
def convert():
    # Get the user input
    amount = amount_entry.get()
    _from = from_var.get()
    to = to_var.get()

# Taxation idea and fun seize ftn from Zion, code structured by zion, changed to consider CAD value by and consider the remainder by SJ

    query_params = {"amount": amount, "from": _from, "to": "CAD"}
    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code == 200:
        data = response.json()
        CAD = data['result']
        print(CAD)
    else:
        result_label.config(text="Error: Failed to convert currency")

    # Add a 10% tax if the amount being converted is more than 10,000 CAD
    if float(CAD) > 10000:
        tax_label.config(text="You have been federally taxed 10% on your " + str(amount) + " " + _from)
        amount = float(amount) * 0.9
    else:
        pass

    if Seize == True:
        amount = 0
        seized_label.config(text="The government has seized your funds.")




    # Make the API request
    query_params = {"amount": amount, "from": _from, "to": to}
    response = requests.get(url, headers=headers, params=query_params)

    # Update the result label
    if response.status_code == 200:
        data = response.json()
        result_label.config(text=f"{data['result']:.2f} {to}")
    else:
        result_label.config(text="Error: Failed to convert currency")


# Define the convert button
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.grid(row=5, column=0, columnspan=2)

# Start the GUI loop
root.mainloop()