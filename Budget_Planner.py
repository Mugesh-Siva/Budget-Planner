import os
import sys
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import socket
import webbrowser
import google.generativeai as genai
import urllib.request
monthly_income = 0
total_expenses = 0
expenses_data = []  
remaining_amount = 0 
x_plot=[]
y_plot=[]
remaining_plot=[]
n=0
#AIzaSyAYj7JCsCe0khXu4M-PYaVyjL9o6SJU9b0
def getresponse():
    message=search1.get()
    if not message:
        text_area_ai.config(state=NORMAL)
        text_area_ai.insert(END,f"Your Message was Empty...\n") 
        text_area_ai.insert(END,f"____________________________________________________________________________\n")
        text_area_ai.config(state=DISABLED)
        return
    try:
        connection=urllib.request.urlopen("https://docs.google.com/forms/d/e/1FAIpQLSdqfJ86t9HbLz3Qx9z4hJn06_VhveQUcTjAKbw1P4ZWXGHXpQ/viewform?usp=dialog",timeout=5)
        connection.close()
        search1.delete(0,END)
        genai.configure(api_key="AIzaSyD7dOBNqRdp-GUz214L5ngBpzA7a_WIx3g")
        mymodel=genai.GenerativeModel("gemini-1.5-flash")
        mychat=mymodel.start_chat()
        response=mychat.send_message(f"Now you are in my Budget Planner application. This application is for calculating the total expenses for events such as marrage functions,tours,party and other important events.Dont discuss about any events by yourself until i give reference about it. just help generally. It is not based on monthly income or spendings. you need to help me in such a way that i can plan my spendings on events.help me what are the basic needs of every events and how much i can allocate on each needs as per the message follows{message} give a clear replay without using more empty spaces without multiple newlines or white spaces")
        text_area_ai.configure(state=NORMAL)
        text_area_ai.insert(END,f"AI Response : \n{response.text}\n")
        text_area_ai.insert(END,f"____________________________________________________________________________\n")
        text_area_ai.configure(state=DISABLED)
    except urllib.request.URLError:
        text_area_ai.config(state=NORMAL)
        text_area_ai.insert(END,f"Check your Internet Connection\n")
        text_area_ai.insert(END,f"____________________________________________________________________________\n")
        text_area_ai.config(state=DISABLED) 
def textwithai():
    m = 0
    global ai, search1, text_area_ai
    ai = Toplevel(start)
    ai.iconbitmap(resource_path('resources/icon.ico'))

    ai.config(bg="steel blue")
    screen_width = ai.winfo_screenwidth()
    screen_height = ai.winfo_screenheight()
    ai.geometry(f"{screen_width}x{screen_height}")
    for i in range(50):
        root.rowconfigure(i, weight=1)
        root.columnconfigure(i, weight=1)
    text_area_ai = ScrolledText(ai, wrap=WORD, width=81, height=19, font=("Verdana", 15), bg="steel blue4", fg="black")
    text_area_ai.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    top_frame1 = Frame(ai, bg="steel blue")
    top_frame1.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)
    search_label1 = Label(top_frame1, text="Ask Here : ", font=("Verdana", 19), bg="steel blue", fg="black")
    search_label1.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
    search1 = Entry(top_frame1, borderwidth=5, font=("Comic Sans MS", 15), bg="steelblue2", width=50, fg="black")
    search1.grid(row=0, column=2, padx=(5, 5), pady=5, sticky="w")
    del_his1 = Button(top_frame1, text="Get Response", command=lambda: check_entry_and_execute(), font=("Verdana", 15), borderwidth=5, bg="steel blue4", fg="black")
    del_his1.grid(row=0, column=4, padx=(5, 0), pady=5, sticky="w")
    if m == 0:
        text_area_ai.insert(END, f"How May I Assist You Today With Your Budget Planning Needs?\n")
        text_area_ai.insert(END,f"____________________________________________________________________________\n")

        m += 1
    text_area_ai.config(state=DISABLED)
    search1.bind("<Return>", lambda event: check_entry_and_execute())
def check_entry_and_execute():
    getresponse()  
def openlink():
    url="https://docs.google.com/forms/d/e/1FAIpQLSdqfJ86t9HbLz3Qx9z4hJn06_VhveQUcTjAKbw1P4ZWXGHXpQ/viewform?usp=dialog"
    webbrowser.open(url)
def resetall():
    global root,history_window,summary_window,contact_page,start,contact,x_plot,y_plot,monthly_income,expenses_data,remaining_amount,total_expenses,n,ai
    monthly_income=0
    x_plot=[]
    y_plot=[]
    expenses_data=[]
    remaining_amount=0
    total_expenses=0
    n=0
    dummywindow=Toplevel(root)
    history_window=dummywindow
    summary_window=dummywindow
    contact_page=dummywindow
    start=dummywindow
    contact=dummywindow
    ai=dummywindow
    if history_window.winfo_exists():
        history_window.destroy()
    if summary_window.winfo_exists():
        summary_window.destroy()
    if contact_page.winfo_exists():
        contact_page.destroy()
    if start.winfo_exists():
        start.destroy()
    if contact.winfo_exists():
        contact.destroy()
    if ai.winfo_exists():
        ai.destroy()
    if root.winfo_exists():
        root.destroy()
    
    create_summary_table()
    main()
def feedback_entry():
    global name, email, feedback
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    feedback = feedback_text.get("1.0", END).strip()
    if not name or not email or not feedback:
        messagebox.showerror("Incomplete input", "Please enter all the input fields before continuing.", parent=contact)
        return
    messagebox.showinfo("Sucess","Your feedback was recived sucessfully")
    save_feedback()
def on_enter_press(event):
    if name_entry.get():
        email_entry.focus_set()
    if email_entry.get():
        feedback_text.focus_set()
def save_feedback():
    global name ,email,feedback
    SERVER_IP = "XXX.XXX.XXX.XXX"  
    SERVER_PORT = 12345            
    message = f"Name: {name}\nEmail: {email}\nFeedback: {feedback}"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
def contact_info():
    global contact, name_entry, email_entry, feedback_text
    contact = Toplevel(root)
    contact.title("Feedback Window")
    contact.iconbitmap(resource_path('resources/icon.ico'))
    screen_width = contact.winfo_screenwidth()
    screen_height = contact.winfo_screenheight()
    for i in range(20):
        contact.grid_rowconfigure(i, weight=1)
        contact.grid_columnconfigure(i, weight=1)
    contact.geometry(f"{screen_width}x{screen_height}")
    background_image1 = Image.open(resource_path('resources/black.jpg'))
    background_image1= background_image1.resize((screen_width, screen_height), Image.LANCZOS)
    background_photo1 = ImageTk.PhotoImage(background_image1)
    canvas = tk.Canvas(contact, width=screen_width, height=screen_height)
    canvas.place(x=0, y=0) 
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo1)
    name_label = Label(contact, text="Enter Your Name  : ", font=("Comic Sans MS", 25), bg="black",fg="steel blue1")
    name_entry = Entry(contact, borderwidth=1, font=("Comic Sans MS", 20), fg="steel blue4",bg="steel blue3")
    email_label = Label(contact, text="Enter Your Email  : ", font=("Comic Sans MS", 25), fg="steel blue1", bg="black")
    email_entry = Entry(contact, font=("Comic Sans MS", 20), fg="steel blue3", bg="steel blue4")
    feedback_label = Label(contact, text="   FeedBack ➡️", font=("Comic Sans MS", 35), fg="steel blue1", bg="black")
    feedback_text = Text(contact, width=80, height=20, font=("Helvetica", 11), fg="steel blue3", bg="steel blue4")
    submit_button = Button(contact, text="Submit", command=feedback_entry, height=2, width=10, borderwidth=6,font=("verdana", 14), bg="black",fg="steel blue2")
    contact.bind('<Return>', on_enter_press)
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    email_label.grid(row=2, column=0)
    email_entry.grid(row=2, column=1)
    feedback_label.grid(row=3, column=0)
    feedback_text.grid(row=3, column=1)
    submit_button.grid(row=7, column=1)
    contact.mainloop()
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def save_income(event=None):
    global monthly_income, remaining_amount,plan_name
    if not enter_amount.get().isdigit() or not enter_nbutton.get():
        messagebox.showerror("Improper Input Error","Please enter a valid input for both feilds", parent=start)
    else:
        plan_name=enter_nbutton.get()
        monthly_income = int(enter_amount.get())
        remaining_amount = monthly_income
        income_label.grid_remove()
        enter_amount.grid_remove()
        enter_button.grid_remove()
        enter_ai.grid_remove()
        enter_name.grid_remove()
        enter_nbutton.grid_remove()
        expense_label.grid(row=8, column=10)
        expense_entry.grid(row=8, column=11)
        purpose_label.grid(row=10, column=10)
        purpose_entry.grid(row=10, column=11)
        visualize_button.grid(row=12,column=10)
        remaining_label.grid(row=12, column=11, columnspan=1)
        reset_button.grid(row=16,column=10)
        end_button.grid(row=14, column=11)
        reset_button.grid(row=14,column=10)
        info_button.grid(row=16,column=10)
        save_button.grid(row=16,column=11)
        update_remaining_label()
        start.unbind('<Return>')
        start.bind('<Return>', save_expense)
def showhint():
    messagebox.showinfo("Press Enter Key","Press Enter Key to Keep Record of the Values You Entered",parent=start)
def save_expense(event=None):
    global total_expenses, expenses_data, remaining_amount,expense_amount,expense_purpose,x_plot,y_plot,n,expense_dict
    if not expense_entry.get() or not purpose_entry.get():
        messagebox.showerror("Incomplete input Error", "Please enter both the expense amount and the purpose.", parent=start)
        return  
    if purpose_entry.get() in x_plot:
        messagebox.showerror("Already exist Error","The Purpose you entered already exist.",parent=start)
        return
    try:
        expense_amount = int(expense_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid integer for the expense amount.", parent=start)
        return
    expense_purpose = purpose_entry.get()
    expense_dict={}
    expense_dict.update({expense_purpose:expense_amount})
    total_expenses += expense_amount
    expenses_data.append((expense_amount , expense_purpose))
    append_amount=remaining_amount-expense_amount
    remaining_amount -= expense_amount
    if remaining_amount<0:
        if n==0:
            y_plot.append(expense_amount)
            n=n+1
        else:
            y_plot.append(-abs(expense_amount))
    else:
        y_plot.append(expense_amount)
    update_remaining_label()
    expense_entry.delete(0, END)
    purpose_entry.delete(0, END)
    x_plot.append(expense_purpose)
def update_remaining_label():
    remaining_label.config(text=f"Remaining Amount: ${remaining_amount}")
def validate_integer(value):
    return value.isdigit() or value == ""
def on_select(event):
    """Callback function for handling dropdown selection."""
    selected_option = visualize_button.get()
    # Map the selection to the appropriate function
    options_map = {
        "Barchart": barchart,
        "Graph": graph,
        "Piechart":piechart,
    }
    if selected_option in options_map:
        options_map[selected_option]()
def expense_enter():
    global expense_entry, purpose_entry, enter_amount, income_label, enter_button, end_button, start, bg_photo_start, remaining_label,visualize_button,info_button,reset_button,start,expense_label_row,expense_label_col,info_button_row,info_button_col,purpose_label_row,purpose_label_col,enter_ai
    global expense_label, expense_entry_row, expense_entry_col, purpose_label, purpose_entry_row, purpose_entry_col, end_button_row, end_button_col, remaining_label_row, remaining_label_col,visualize_button_col,visualize_button_row,info_button,reset_button,save_button,save_button_col,save_button_row
    global monthly_income,x_plot,y_plot,expenses_data,remaining_amount,total_expenses,n,imageid,enter_name,enter_nbutton
    if any(widget.winfo_name()=="start" for widget in root.winfo_children()):
        plt.close('all')
        start.destroy()
    monthly_income=0
    x_plot=[]
    y_plot=[]
    expenses_data=[]
    remaining_amount=0
    total_expenses=0
    n=0
    start = tk.Toplevel(root,name="start")
    start.title("Budget planner")
    screen_width =start.winfo_screenwidth()
    screen_height = start.winfo_screenheight()
    start.geometry(f"{screen_width}x{screen_height}")
    start.iconbitmap(resource_path('resources/icon.ico'))
    for i in range(25):
        start.grid_rowconfigure(i, weight=1)
        start.grid_columnconfigure(i, weight=1)
    bg_img_start = Image.open(resource_path('resources/resize.jpg'))
    bg_img_start=bg_img_start.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo_start = ImageTk.PhotoImage(bg_img_start)
    canvas = tk.Canvas(start, width=screen_width, height=screen_height)
    canvas.place(x=0, y=0) 
    imageid=canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo_start)
    income_label = Label(start, text="Enter your budget amount",bg="black",fg="cyan", width=0, height=0, font=("Comic Sans MS", 30))
    vcmd = (start.register(validate_integer), '%P')
    enter_amount = Entry(start, width=15, borderwidth=4, validate='key', validatecommand=vcmd, font=("Verdana", 24),bg="steel blue1")
    enter_button = Button(start, text="Confirm", command=save_income, width=0, height=0, font=("Verdana", 20),borderwidth=9,bg="steel blue2")
    enter_ai = Button(start, text="Get AI Insights", command=textwithai, width=0, height=0, font=("Verdana", 20),borderwidth=9,bg="steel blue2")
    enter_name=Label(start, text="Give a name for your plan",bg="black",fg="cyan", width=0, height=0, font=("Comic Sans MS", 30))
    enter_nbutton= Entry(start, width=15, borderwidth=4,font=("Verdana", 24),bg="steel blue1")
    end_button = Button(start, text="Go To Summary", command=display_data, width=0, height=1, font=("Verdana", 19),borderwidth=9,bg="black",fg="cyan")
    remaining_label = Label(start, text="Remaining Amount ", width=0, height=0, font=("Comic Sans MS", 22),bg="black",fg="cyan")
    expense_label = Label(start, text="Expense Amount      ➡️", font=("Comic Sans MS", 22),bg="black",fg="cyan")
    expense_entry = Entry(start, validate='key', validatecommand=vcmd, borderwidth=5, width=17, font=("Comic Sans MS", 20),bg="steelblue3")
    purpose_label = Label(start, text="Purpose Of Expense ➡️", font=("Comic Sans MS", 22),bg="black",fg="cyan")
    purpose_entry = Entry(start, borderwidth=5, width=17, font=("Comic Sans MS", 20),bg="steel blue3")
    reset_button=Button(start, text="Plan a New Budget", command=resetall, width=0, height=1, font=("Verdana", 19),borderwidth=9,bg="black",fg="cyan")
    info_button =Button(start, text="Hint🗝️", command=showhint, width=0, height=1, font=("Verdana", 19),borderwidth=9,bg="black",fg="cyan")
    save_button=Button(start, text="Save Your Plan", command=save, width=0, height=1, font=("Verdana", 19),borderwidth=9,bg="black",fg="cyan")
    options = ["Barchart", "Graph","Piechart"]
    mystyle=ttk.Style()
    mystyle.configure(
        "Custom.TCombobox",
        foreground="Black",
        background="black",
        feildbackground="black",
    )
    visualize_button = ttk.Combobox(start, values=options, state="readonly",font=("Verdana", 20),style="Custom.TCombobox")
    visualize_button.grid(row=12,column=10)
    visualize_button.set("Data visualization")  # Default text
    visualize_button.bind("<<ComboboxSelected>>", on_select)
    income_label.grid(row=10, column=11)
    enter_amount.grid(row=10, column=12)
    enter_name.grid(row=12,column=11)
    enter_nbutton.grid(row=12,column=12)
    enter_button.grid(row=16, column=12)
    enter_ai.grid(row=16,column=11)
    save_button_row,save_button_col=12,11
    info_button_row,info_button_col=12,10
    expense_label_row, expense_label_col = 14, 10
    expense_entry_row, expense_entry_col = 14, 11
    purpose_label_row, purpose_label_col = 15, 10
    purpose_entry_row, purpose_entry_col = 15, 11
    end_button_row, end_button_col = 16, 10
    remaining_label_row, remaining_label_col = 17, 10
    start.bind('<Return>', save_income)
    info_button.grid_remove()
    expense_label.grid_remove()
    expense_entry.grid_remove()
    purpose_label.grid_remove()
    purpose_entry.grid_remove()
    end_button.grid_remove()
    remaining_label.grid_remove()
    visualize_button.grid_remove()
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def Contact_page_pkg():
    global contact_page,label1_cp,label2_cp,label3_cp,label4_cp,label5_cp,label6_cp,button1_cp  

    if any(widget.winfo_name()=="contact_page" for widget in root.winfo_children()):
        contact_page.destroy()
    contact_page=Toplevel(root,name="contact_page")
    contact_page.configure(bg="gray45")
    contact_page.title("Contact us")
    contact_page.iconbitmap(resource_path('resources/icon.ico'))
    for a in range (20):
        contact_page.rowconfigure(a,weight=1)
        contact_page.columnconfigure(a,weight=1)
    screen_width = contact_page.winfo_screenwidth()
    screen_height = contact_page.winfo_screenheight()
    contact_page.geometry(f"{screen_width}x{screen_height}")
    background_img= Image.open(resource_path('resources/contactus.jpg'))
    background_img= background_img.resize((screen_width, screen_height), Image.LANCZOS)
    background_ph= ImageTk.PhotoImage(background_img)
    canvas = tk.Canvas(contact_page, width=screen_width, height=screen_height)
    canvas.place(x=0, y=0)  # Use place() instead of grid()
    canvas.create_image(0, 0, anchor=tk.NW, image=background_ph)
    label1_cp=Label(contact_page,text="Contact details",font=("ariel", 30,"italic"),bg="black",fg="steel blue1")
    label2_cp=Label(contact_page,text="E-mail : hmsolutions.tech.pvt@gmail.com",font=("Comic Sans MS", 20, "italic"),bg="black",fg="steel blue1")
    label3_cp=Label(contact_page,text="Contact Number : +91 96777 99848",font=("Comic Sans MS", 20, "italic"),bg="black",fg="steel blue1")
    label4_cp=Label(contact_page,text="Help Us Improve !",font=("Comic Sans MS", 25),bg="black",fg="steel blue")
    label5_cp=Label(contact_page,text="Give Your Feedback Below",font=("Comic Sans MS", 20, ),bg="black",fg="steel blue1")
    button1_cp=Button(contact_page,text="Go to Feedback",font=("Comic Sans MS", 19),bg="black",fg="steel blue1",borderwidth=9,command=openlink)
    label6_cp=Label(contact_page,text="(The above button leads to feedback page)",font=("Comic Sans MS", 10, "italic"),bg="black",fg="steel blue1")
    label1_cp.grid(row=6,column=10)
    label2_cp.grid(row=8,column=10)
    label3_cp.grid(row=9,column=10)
    label4_cp.grid(row=10,column=10)
    label5_cp.grid(row=11,column=10)
    button1_cp.grid(row=12,column=10)
    label6_cp.grid(row=13,column=10)
    contact_page.mainloop()
def save_summary(monthly_income, total_expenses, remaining_amount, expenses_details):
    conn = sqlite3.connect('BudgetPlanner.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO Budget_summary (name,income, expenses, remaining, details)
        VALUES (?, ?, ?, ?, ?)
    ''', (plan_name,monthly_income, total_expenses, remaining_amount, expenses_details))
    conn.commit()
    conn.close()
def display_data():
    global monthly_income, total_expenses, expenses_data, remaining_amount,summary_window
    if any(widget.winfo_name()=="summary_window" for widget in root.winfo_children()):
        summary_window.destroy()
    #expenses_details = "\n".join([f"Purpose: {purpose}, Amount: ${amount}" for amount, purpose in expenses_data])
    #save_summary(monthly_income, total_expenses, remaining_amount, expenses_details)
    summary_window = Toplevel(root,name="summary_window")
    summary_window.title("YOUR BUDGET SUMMARY - Summary")
    summary_window.configure(bg="steel blue4") 
    text_area = ScrolledText(summary_window, wrap=WORD, width=81, height=19, font=("Verdana", 17), bg="deep skyblue4")  
    text_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    text_area.insert(END, f"Your Plan Name : {enter_nbutton.get()}\n", ("bold",))
    text_area.insert(END, f"YOUR TOTAL BUDGET: ${monthly_income}\n", ("bold",))
    text_area.insert(END, f"TOTAL EXPENSES: ${total_expenses}\n", ("bold",))
    text_area.insert(END, f"REMAINING AMOUNT: ${remaining_amount}\n\n", ("bold",))
    text_area.insert(END, "EXPENSES DETAILS:\n", ("bold",))
    for i, (amount, purpose) in enumerate(expenses_data):
        text_area.insert(END, f"{i + 1}. Purpose: {purpose}, Amount: ${amount}\n", ("normal",))
    text_area.insert(END,f"\n",("bold",))
    text_area.config(state=DISABLED)
    text_area.tag_configure("bold", font=("Comic Sans MS", 17))
    text_area.tag_configure("normal", font=("Comic Sans MS", 17))
    text_area.config(state=DISABLED)
def barchart():
    plt.close('all')
    global monthly_income, x_plot, y_plot
    original_monthly_income = monthly_income
    original_x_plot = x_plot[:]
    original_y_plot = y_plot[:]
    adjusted_x_plot = []
    adjusted_y_plot = []
    for label, value in zip(x_plot, y_plot):
        if value > 0 and value <= monthly_income:
            adjusted_x_plot.append(label)
            adjusted_y_plot.append(value)
            monthly_income -= value
        elif value > monthly_income:
            positive_part = monthly_income
            negative_part = value - monthly_income
            if positive_part > 0:  
                adjusted_x_plot.append(label)
                adjusted_y_plot.append(positive_part)
            summa ="--"+ label 
            adjusted_x_plot.append(summa)  
            adjusted_y_plot.append(-negative_part)
            monthly_income = 0
        elif value < 0:
            adjusted_x_plot.append(f'-{label}')
            adjusted_y_plot.append(value)
    colors = ['blue' if val > 0 else 'red' for val in adjusted_y_plot]
    plt.bar(
        adjusted_x_plot,
        adjusted_y_plot,
        color=colors,
        edgecolor="black"
    )
    plt.axhline(0, color='black', linewidth=0.8) 
    plt.title("Bar Chart of Expenses\n(Note : The Items With Negative Amount Have  '--' In Front)")
    plt.xlabel("Categories")
    plt.ylabel("Values")
    monthly_income = original_monthly_income
    x_plot = original_x_plot
    y_plot = original_y_plot
    plt.show()
def graph():
    plt.close('all')
    global monthly_income, x_plot, y_plot
    original_monthly_income = monthly_income
    original_x_plot = x_plot[:]
    original_y_plot = y_plot[:]
    adjusted_x_plot = []
    adjusted_y_plot = []
    for label, value in zip(x_plot, y_plot):
        if value > 0 and value <= monthly_income:
            adjusted_x_plot.append(label)
            adjusted_y_plot.append(value)
            monthly_income -= value
        elif value > monthly_income:
            positive_part = monthly_income
            negative_part = value - monthly_income
            if positive_part > 0:  
                adjusted_x_plot.append(label)
                adjusted_y_plot.append(positive_part)
            summa ="--" +label 
            adjusted_x_plot.append(summa) 
            adjusted_y_plot.append(-negative_part)
            monthly_income = 0
        elif value < 0:
            adjusted_x_plot.append(f'--{label}')
            adjusted_y_plot.append(value)
    colors = ['blue' if val > 0 else 'red' for val in adjusted_y_plot]
    plt.scatter(
        adjusted_x_plot,
        adjusted_y_plot,
        c=colors,
        edgecolor="black",
        s=100  
    )
    negative_start_index = next((i for i, val in enumerate(y_plot) if val < 0), len(y_plot))
    for i in range(1, len(adjusted_x_plot)):
        if i - 1 >= negative_start_index - 1:  
            line_color = 'red'
        else:
            line_color = 'blue' if adjusted_y_plot[i - 1] > 0 else 'red'
        plt.plot(
            [adjusted_x_plot[i - 1], adjusted_x_plot[i]],
            [adjusted_y_plot[i - 1], adjusted_y_plot[i]],
            color=line_color,
            linewidth=2
        )
    plt.axhline(0, color='black', linewidth=0.8) 
    plt.title("Graph of Expenses\n(Note : The Items With Negative Amount Have  '--' In Front)")
    plt.xlabel("Categories")
    plt.ylabel("Values")
    plt.xticks(rotation=45) 
    plt.grid(True, linestyle="--", alpha=0.6)  
    monthly_income = original_monthly_income
    x_plot = original_x_plot
    y_plot = original_y_plot
    plt.show()
def piechart():
    plt.close('all')
    global monthly_income, x_plot, y_plot
    original_monthly_income = monthly_income
    original_x_plot = x_plot[:]
    original_y_plot = y_plot[:]
    adjusted_x_plot = []
    adjusted_y_plot = []
    for label, value in zip(x_plot, y_plot):
        if value > 0 and value <= monthly_income:
            adjusted_x_plot.append(label)
            adjusted_y_plot.append(value)
            monthly_income -= value
        elif value > 0 and value > monthly_income:
            positive_part = monthly_income
            negative_part = value - monthly_income
            if positive_part > 0:  
                adjusted_x_plot.append(label)
                adjusted_y_plot.append(positive_part)
            summa = "--"+label   
            adjusted_x_plot.append(summa)
            adjusted_y_plot.append(-negative_part)
            monthly_income = 0
        elif value < 0:
            adjusted_x_plot.append(f'--{label}')
            adjusted_y_plot.append(value)
    colors = ['green' if val > 0 else 'red' for val in adjusted_y_plot]
    labels = [
        f'{name} ({abs(val)})' for name, val in zip(adjusted_x_plot, adjusted_y_plot)
    ]
    plt.pie(
        [abs(val) for val in adjusted_y_plot],
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={"edgecolor": "black"}
    )
    plt.title("Pie Chart of Expenses\n(Note : The Items With Negative Amount Have  '--' In Front)")
    monthly_income = original_monthly_income
    x_plot = original_x_plot
    y_plot = original_y_plot
    plt.show()
   

def delhis():
    """Delete all records from the summary table and refresh history window."""
    try:
        con = sqlite3.connect('BudgetPlanner.db')
        curser = con.cursor()
        curser.execute('DELETE FROM Budget_summary') 
        curser.execute('DELETE FROM sqlite_sequence WHERE name="Budget_summary"')
        con.commit()
    except sqlite3.Error as e:
        print(f"Error deleting records: {e}")
    finally:
        con.close()
    history_window.destroy()
def show_summary_history():
    """Show the summary history in a new window."""
    global history_window, records  
    def search_records(event):
        """Filter records based on search input."""
        query = search.get().lower()
        text_area.config(state=NORMAL)
        text_area.delete(1.0, END)
        if query:
            filtered_records = [record for record in records if query in record[0].lower()]
            if filtered_records:
                for record in filtered_records:
                    text_area.insert(END, 
                                     f"Sno: {record[1]}\n"
                                     f"Plan name : {record[0]}\n"
                                      f"Total Amount: ${record[2]}\n"
                                      f"Total Expenses: ${record[3]}\nRemaining Amount: ${record[4]}\n"
                                      f"Expenses Details:\n{record[5]}\n\n" 
                                    )
            else:
                text_area.insert(END, "No matching records found.")
        else:
            for record in records:
                text_area.insert(END, 
                                    f"Sno: {record[1]}\n"
                                    f"Plan name : {record[0]}\n"
                                      f"Total Amount: ${record[2]}\n"
                                      f"Total Expenses: ${record[3]}\nRemaining Amount: ${record[4]}\n"
                                      f"Expenses Details:\n{record[5]}\n\n" 
                                    )
        text_area.config(state=DISABLED)
    def delhis():
        try:
            conn = sqlite3.connect('BudgetPlanner.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Budget_summary')
            cursor.execute('DELETE FROM sqlite_sequence WHERE name="Budget_summary"')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting records: {e}")
        finally:
            conn.close()
        text_area.config(state=NORMAL)
        text_area.delete(1.0, END)
        text_area.insert(END, "No summary records found.")
        text_area.config(state=DISABLED)
        del_his.config(state=DISABLED)
        search.config(state=DISABLED)
    if any(widget.winfo_name()=="history_window" for widget in root.winfo_children()):
        history_window.destroy()
    history_window = Toplevel(root,name="history_window")

    history_window.title("Your History")
    screen_width =history_window.winfo_screenwidth()
    screen_height = history_window.winfo_screenheight()
    history_window.geometry(f"{screen_width}x{screen_height}")
    for i in range(10):
        history_window.rowconfigure(i, weight=1)  
    history_window.columnconfigure(0, weight=1)   
    history_window.iconbitmap(resource_path('resources/icon.ico'))
    history_window.configure(bg="skyblue")
    text_area = ScrolledText(history_window, wrap=WORD, width=81, height=19,font=("Verdana", 15), bg="steel blue1", fg="Black")
    text_area.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    try:
        conn = sqlite3.connect('BudgetPlanner.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Budget_summary')
        records = cursor.fetchall()
    except sqlite3.Error as e:
        text_area.insert(END, f"Error fetching records: {e}")
        records = []
    finally:
        conn.close()
    if records:
        top_frame = Frame(history_window, bg="skyblue")
        top_frame.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)
        search_label = Label(top_frame, text="Search by plan name:", font=("Verdana", 19), bg="skyblue")
        search_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        search = Entry(top_frame, borderwidth=5, font=("Comic Sans MS", 15), bg="steelblue1", width=25)
        search.grid(row=0, column=1, padx=(5, 5), pady=5, sticky="w")
        search.bind("<KeyRelease>", search_records)
        del_his = Button(top_frame, text="Delete All Records", command=delhis, font=("Verdana", 15), borderwidth=5, bg="skyblue", fg="Black")
        del_his.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="w")
        for record in records:
            text_area.insert(END, f"Sno : {record[1]}\n"
                              f"Plan Name :{record[0]}\n"
                              f"Total Amount: ${record[2]}\n"
                              f"Total Expenses: ${record[3]}\nRemaining Amount: ${record[4]}\n"
                              f"Expenses Details:\n{record[5]}\n\n")
    else:
        top_frame = Frame(history_window, bg="skyblue")
        top_frame.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)
        search_label = Label(top_frame, text="Search by plan name:", font=("Verdana", 19), bg="skyblue",fg="black")
        search_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        search = Entry(top_frame, borderwidth=5, font=("Comic Sans MS", 15), bg="steel blue4", width=25,state=DISABLED)
        search.grid(row=0, column=1, padx=(5, 5), pady=5, sticky="w")
        del_his = Button(top_frame, text="Delete All Records", command=delhis, font=("Verdana", 15), borderwidth=5, bg="skyblue", fg="Black",state=DISABLED)
        del_his.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="w")
        text_area.insert(END, "No summary records found.")
    text_area.config(state=DISABLED)
def create_summary_table():
    conn = sqlite3.connect('BudgetPlanner.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Budget_summary (
            name TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income INTEGER,
            expenses INTEGER,
            remaining INTEGER,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()
def save():
    expenses_details = "\n".join([f"Purpose: {purpose}, Amount: ${amount}" for amount, purpose in expenses_data])
    save_summary(monthly_income, total_expenses, remaining_amount, expenses_details)
    messagebox.showinfo("Saved Sucessfully","Your Plan was Saved Sucessfully",parent=start)
def main():
    global root,button1,button2,button3,rootimg
    root=Tk()
    root.title("Budget Planner")
    screen_width =root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    for i in range(50):
        root.rowconfigure(i,weight=1)
        root.columnconfigure(i,weight=1)
    background_image = Image.open(resource_path('resources/main.jpg'))
    background_image= background_image.resize((screen_width, screen_height), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.place(x=0, y=0)  # Use place() instead of grid()
    rootimg=canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    root.iconbitmap(resource_path('resources/icon.ico'))
#label1=Label(root,text="💲Budget Planner💲",font=("Comic Sans MS", 35),bg="snow2",fg="gray25",borderwidth=8)
#label2=Label(root,text="Start Planning Your Budget",font=("Comic Sans MS", 35),fg="cadetblue1",bg="gray44")
    button1=Button(root,text="Start Planning",font=("Comic Sans MS", 22),fg="black",bg="cyan4",borderwidth=9,command=expense_enter)
    button3=Button(root,text="Contact Us",font=("Comic Sans MS", 19),fg="black",bg="cyan4",borderwidth=9,command=Contact_page_pkg)
    button2=Button(root,text="History",font=("Comic Sans MS", 17),fg="black",bg="cyan4",borderwidth=9,command=show_summary_history)
#label1.grid(row=6,column=10)
#label2.grid(row=7,column=14)
    button1.grid(row=31,column=24)
    button3.grid(row=33,column=24)
    button2.grid(row=35,column=24)
    root.mainloop()
    try:
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
create_summary_table()
main()
