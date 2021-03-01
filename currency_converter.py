import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
import re


class currency_convert():
    def __init__(self,url):
            self.data = requests.get(url).json()
            self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
  
        amount = round(amount * self.currencies[to_currency], 3) # Upto 3 decimal
        return amount

class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'
        self.currency_converter = converter
        self.configure(background = '#010606')
        self.geometry("600x250")
        
        # Title(Label)
        self.intro_label = Label(self, text = 'Currency Converter', fg = '#39ff14', bg = '#010606')
        self.intro_label.config(font = ('Courier',15,'bold'))
        self.date_label = Label(self, text = f"1 USD = {self.currency_converter.convert('USD','INR',1)} INR \n Date : {self.currency_converter.data['date']}")
        self.intro_label.place(x = 210, y = 5)
        self.date_label.place(x = 230, y= 50)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self,bd = 3, relief = tk.RIDGE, justify = tk.CENTER,validate='key', validatecommand=valid)
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 17, borderwidth = 3)

        # Currency List
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("USD") # Default value for 1st Currency List
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("INR") # Default value for 2nd Currency List
        font = ("Courier", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)

        # Placement of Currency List and amount field
        self.from_currency_dropdown.place(x = 75, y= 120)
        self.amount_field.place(x = 30, y = 150)
        self.to_currency_dropdown.place(x = 420, y= 120)
        self.converted_amount_field_label.place(x = 390, y = 150)
        
        # Convert button
        self.convert_button = Button(self, text = "Convert", fg = "black", command = self.perform) 
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x = 260, y = 150)

        # Footer(Label)
        self.footer_label = Label(self, text = 'By Chandan Choudhury', fg = '#39ff14', bg = '#010606')
        self.footer_label.config(font = ('Courier',15,'bold'))
        self.footer_label.place(x = 400, y = 220)

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()
        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 2)
        self.converted_amount_field_label.config(text = str(converted_amount))
    
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = currency_convert(url)

    App(converter)
    mainloop()