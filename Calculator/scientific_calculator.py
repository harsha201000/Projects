from tkinter import *
import math

# ----------------- Calculator Functions -----------------
def button_press(num):
    global equation_text
    equation_text += str(num)
    equation_label.set(equation_text)

def clear():
    global equation_text
    equation_text = ""
    equation_label.set("")

def equals():
    global equation_text
    try:
        # evaluate scientific functions
        total = eval(equation_text)
        if total % 1 == 0:
            total = int(total)
        equation_label.set(total)
        equation_text = str(total)
    except ZeroDivisionError:
        equation_label.set("ARITHMETIC ERROR")
        equation_text = ""
    except:
        equation_label.set("SYNTAX ERROR")
        equation_text = ""

def percent():
    global equation_text
    try:
        result = float(equation_text) / 100
        equation_label.set(result)
        equation_text = str(result)
    except:
        equation_label.set("ERROR")
        equation_text = ""

def toggle_sign():
    global equation_text
    try:
        number = float(equation_text) * -1
        equation_label.set(number)
        equation_text = str(number)
    except:
        equation_label.set("ERROR")
        equation_text = ""

def delete():
    global equation_text
    equation_text = equation_text[:-1]
    equation_label.set(equation_text)

def apply_scientific(func):
    global equation_text
    try:
        num = float(equation_text)
        if func == "sin":
            result = math.sin(math.radians(num))
        elif func == "cos":
            result = math.cos(math.radians(num))
        elif func == "tan":
            result = math.tan(math.radians(num))
        elif func == "log":
            result = math.log10(num)
        elif func == "ln":
            result = math.log(num)
        elif func == "sqrt":
            result = math.sqrt(num)
        elif func == "fact":
            result = math.factorial(int(num))
        elif func == "exp":
            result = math.exp(num)
        equation_label.set(result)
        equation_text = str(result)
    except:
        equation_label.set("ERROR")
        equation_text = ""

def apply_conversion():
    global equation_text
    try:
        value = float(equation_text)
        if conversion_var.get() == "USD_to_EUR":
            result = value * 0.91  # example rate
        elif conversion_var.get() == "EUR_to_USD":
            result = value * 1.1
        elif conversion_var.get() == "KM_to_Miles":
            result = value * 0.621371
        elif conversion_var.get() == "Miles_to_KM":
            result = value * 1.60934
        equation_label.set(result)
        equation_text = str(result)
    except:
        equation_label.set("ERROR")
        equation_text = ""

# ----------------- Main Window -----------------
app = Tk()
app.title("iOS 26 Calculator")
app.geometry("500x600")
app.config(bg="lightgray")

equation_text = ""
equation_label = StringVar()

icon = PhotoImage(file='calc_logo.png')
app.iconphoto(True, icon)

label = Label(app, textvariable=equation_label, font=("Arial", 24), bg="lightgray", width=24, height=2, anchor='e')
label.pack(pady=10)

# ----------------- Button Frame -----------------
frame = Frame(app, bg="lightgray")
frame.pack()

# Numeric Buttons
buttons = [
    ('7',1,0), ('8',1,1), ('9',1,2),
    ('4',2,0), ('5',2,1), ('6',2,2),
    ('1',3,0), ('2',3,1), ('3',3,2),
    ('0',4,1), ('.',4,0)
]

for (text,r,c) in buttons:
    Button(frame,text=text,height=2,width=6,font=15,fg="white",bg="black", command=lambda t=text: button_press(t)).grid(row=r,column=c)

# Operation Buttons
ops = [('+',3,3), ('-',2,3), ('*',1,3), ('/',0,3), ('=',4,2)]
for (op,r,c) in ops:
    if op == '=':
        Button(frame,text=op,height=2,width=6,font=15,fg="white",bg="orange", command=equals).grid(row=r,column=c)
    else:
        Button(frame,text=op,height=2,width=6,font=15,fg="white",bg="orange", command=lambda t=op: button_press(t)).grid(row=r,column=c)

# Extra Buttons
Button(frame,text='AC',height=2,width=6,font=15,fg="black",bg="lightgrey",command=clear).grid(row=0,column=0)
Button(frame,text='DEL',height=2,width=6,font=15,fg="white",bg="black",command=delete).grid(row=0,column=1)
Button(frame,text='%',height=2,width=6,font=15,fg="black",bg="lightgrey",command=percent).grid(row=0,column=2)
Button(frame,text='+/-',height=2,width=6,font=15,fg="black",bg="lightgrey",command=toggle_sign).grid(row=4,column=3)

# ----------------- Scientific Buttons -----------------
sci_frame = Frame(app, bg="lightgray")
sci_frame.pack(pady=10)

scientific = ['sin','cos','tan','log','ln','sqrt','fact','exp']
for i,func in enumerate(scientific):
    Button(sci_frame, text=func, width=6, height=2, bg="darkblue", fg="white", font=12,
           command=lambda f=func: apply_scientific(f)).grid(row=i//4, column=i%4, padx=2, pady=2)

# ----------------- Conversion -----------------
conversion_var = StringVar()
conversion_var.set("USD_to_EUR")
conversion_frame = Frame(app, bg="lightgray")
conversion_frame.pack(pady=10)

Label(conversion_frame, text="Conversions", bg="lightgray", font=12).grid(row=0,column=0,columnspan=2)

conversions = [("USD → EUR", "USD_to_EUR"),
               ("EUR → USD", "EUR_to_USD"),
               ("KM → Miles", "KM_to_Miles"),
               ("Miles → KM", "Miles_to_KM")]

for i,(text,val) in enumerate(conversions):
    Radiobutton(conversion_frame, text=text, variable=conversion_var, value=val, bg="lightgray", font=10).grid(row=i+1,column=0, sticky='w')

Button(conversion_frame, text="Convert", bg="green", fg="white", font=12, width=10, command=apply_conversion).grid(row=1,column=1,rowspan=4,padx=5)

app.mainloop()
