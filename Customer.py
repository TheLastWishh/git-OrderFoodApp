import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from UserData import UserData
import pymysql
import random
from tkinter import messagebox

root = Tk()
root.title('App Order')
root.geometry('1280x720+125+40')
root.config(bg='#DDDDDD')
root.resizable(False, False)
icon_path = "Images/icon.ico"
root.iconbitmap(icon_path)

def connect_serve():
    try:
        global conn
        conn = pymysql.connect(host='localhost', 
                               user='root', 
                               password='1111', 
                               database='manageorder')
    except:
        messagebox.showerror('Error', 'Database Connectivity Issue, Pleasr Try Again')
        return

def sign_out():
    root.destroy()
    import SignIn

def update_scrollbar(event):
    menuCanvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

def reset_scrollbar(event):
    menuCanvas.yview_moveto(0)

def ORDER_ID():
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    random_letters = ""
    random_digits = ""
    for i in range(0,2):
        random_letters += random.choice(letters)
    for i in range(0, 6):
        random_digits += str(random.choice(numbers))

    order_id = random_letters + random_digits
    
    return order_id

def get_balance():
    connect_serve()
    mycursor = conn.cursor()
    query = "SELECT Balance from account where Username=%s"
    mycursor.execute(query, UserData.username)
    balance = mycursor.fetchone()
    mycursor.close
    conn.close()
    return balance

def get_menu():
    connect_serve()
    mycursor = conn.cursor()
    query = "SELECT Name, Price FROM listdish"
    mycursor.execute(query)
    list_dish = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return list_dish

def add_dish(dish_name, dish_price):
    global totalAmount
    treeOrder.insert('', 'end', values=(dish_name, dish_price))
    
    totalAmount += int(dish_price)
    totalLabel.config(text=f"{totalAmount}")

def creat_widget_display_menu():
    rows = 0
    col = 0
    for index in range(0, len(list_dish)):
        dish_name = list_dish[index][0]
        dish_price = list_dish[index][1]
        try:
            image_path = f"Images/{dish_name}.jpg"
            image = Image.open(image_path).resize((190, 190))
            photo = ImageTk.PhotoImage(image)
        except:
            image_path = f"Images/default.jpg"
            image = Image.open(image_path).resize((190, 190))
            photo = ImageTk.PhotoImage(image)
        photo_list.append(photo)  # Store the PhotoImage object in the list
        imageDish_label = tk.Label(displayDishFrame, image=photo, bg='#FFFFFF')
        imageDish_label.grid(row=rows, column=col, padx=5, pady=5)
        rows += 1
        infoDish_label = tk.Label(displayDishFrame, text=f"{dish_name}\n{dish_price} VND", bg='#FFFFFF',
                                  fg='black', font=('Helvetica', 14))
        infoDish_label.grid(row=rows, column=col, padx=5, sticky='NSEW')
        rows += 1
        addButton = tk.Button(displayDishFrame, text='ADD', height=1, bg='#0000FF', fg='#FFFFFF',
                              font=('Helvetica', 14), cursor='hand2', bd=0, 
                              command=lambda name=dish_name, price=dish_price:add_dish(name, price))
        addButton.grid(row=rows, column=col, padx=5, pady=(0, 10), sticky='NSEW')
        if col < 2:
            col += 1
            rows -= 2
        else:
            col = 0
            rows += 3

def delete_dish():
    selected_dish = treeOrder.selection()
    for dishID in selected_dish:
        dish_info = treeOrder.item(dishID)
        global totalAmount
        totalAmount -= int(dish_info['values'][1])
        totalLabel.config(text=f'{totalAmount}')
        treeOrder.delete(dishID)

def delete_all_dish():
    treeOrder.delete(*treeOrder.get_children())
    global totalAmount
    totalAmount = 0
    totalLabel.config(text=f'{totalAmount}')

def get_list_dish():
    data_list = []
    for dish_id in treeOrder.get_children():
        dish_data = treeOrder.item(dish_id, 'values')
        if dish_data:
            data_list.append(tuple(dish_data))
    return data_list

def order_dish():
    def pay_bill(billID, totalAmount):
        def pay_in_cashier():
            mycursor.close()
            conn.close()
            payScreen.destroy()
            messagebox.showinfo('Notification', 'Order Has Been Placed')
        
        def pay_by_balance():
            def pay():
                global balance
                if totalAmount <= balance[0]:
                    query = "UPDATE bill SET PaymentStatus = 'Paid' WHERE BillID = %s"
                    mycursor.execute(query, billID)
                    conn.commit()
                    
                    query = "UPDATE account SET Balance = %s WHERE Username = %s"
                    balanceafterpaid = balance[0]-totalAmount
                    mycursor.execute(query, (balanceafterpaid, UserData.username))
                    conn.commit()
                    
                    payScreen.destroy()
                    
                    query = "SELECT Balance from account where Username=%s"
                    mycursor.execute(query, UserData.username)
                    balance = mycursor.fetchone()
                    balanceLabel.configure(text=f"Balance: {balance[0]}")
                    
                    mycursor.close()
                    conn.close()
                    messagebox.showinfo('Notification', 'Payment Success')
                else:
                    payScreen.destroy()
                    mycursor.close()
                    conn.close()
                    messagebox.showinfo('Notification', 'Balance Is Insufficient, Please Pay At The Cashier')
                    
                    
            payFrame = Frame(payScreen, bg='#FFFFFF', width=340, height=150, bd=1,
                            relief=tk.SOLID, highlightbackground="#00FF00")
            payFrame.place(x=30, y=235)
            
            query = "SELECT Balance from account where Username=%s"
            mycursor.execute(query, UserData.username)
            balance = mycursor.fetchone()
            Label(payFrame, text=f'Balance: {balance[0]}', bg='#FFFFFF', font=('Helvetica', 21, 'bold')).place(x=30, y=20)
            
            Label(payFrame, text=f'Total: {totalAmount}', bg='#FFFFFF', font=('Helvetica', 21, 'bold')).place(x=30, y=60)
            
            payButton = Button(payFrame, text='Pay', bg='#00FFFF', fg='#000000', width=12,
                            font=('Helvetica', 14), cursor='hand2', relief='ridge', command=pay)
            payButton.place(x=100, y=100)
    
        payScreen = Tk()
        payScreen.geometry('400x400+600+200')
        payScreen.configure(bg='#FFFFFF')

        Label(payScreen, text='Select Payment Method', bg='#FFFFFF', font=('Helvetica', 21, 'bold')).place(x=30, y=20)

        payincashierButton = Button(payScreen, text='Payment At The Cashier', bg='#00FFFF', fg='#000000', 
                                width=30, height= 2, font=('Helvetica', 14), 
                                cursor='hand2', relief='ridge', command=pay_in_cashier)
        payincashierButton.place(x=28, y=70)

        paybybalanceButton = Button(payScreen, text='Pay With Account Balance', bg='#00FFFF', fg='#000000', 
                                width=30, height= 2, font=('Helvetica', 14), 
                                cursor='hand2', relief='ridge', command=pay_by_balance)
        paybybalanceButton.place(x=28, y=150)
    
    global totalAmount
    connect_serve()
    mycursor = conn.cursor()
    billID = ORDER_ID()
    data_list_dish_order = get_list_dish()
    table = tableSelect.get()
    if table == '':
        messagebox.showerror('Error', "Haven't Chosen A Table Yet")
        return
    
    count_dict = {}
    for item in data_list_dish_order:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    
    list_dish_order = [(key[0], key[1], count_dict[key], table) for key in count_dict]
    
    query = 'INSERT INTO Bill (BillID, Username, TableOrder, TotalPrice) values (%s, %s, %s, %s)'
    mycursor.execute(query, (billID, UserData.username, table, totalAmount))
    conn.commit()
    for info in list_dish_order:
        query = 'INSERT INTO BillDetail (BillID, Name, Quantity) values (%s, %s, %s)'
        mycursor.execute(query, (billID, info[0], info[2]))
        conn.commit()
        
    pay_bill(billID, totalAmount)
    tableSelect.delete(0, END)
    delete_all_dish()

########--------------------------------------------------------------------------------------------
s = ttk.Style()
s.configure('BannerFrame.TFrame', background='#3366CC')
s.configure('TaskbarFrame.TFrame', background='#FFFFFF')
s.configure('MenuFrame.TFrame', background='#FFFFFF')
s.configure('DisplayMenuFrame.TFrame', background='#FFFFFF')
s.configure('OrderFrame.TFrame', background='#FFFFFF')
s.configure('MenuOrderFrame.TFrame', background='#99FF33')
s.configure("Treeview", font=("Helvetica", 14))

####-------------------------------------Banner------------------------------------------------
bannerFrame = ttk.Frame(root, width=250, height=720, style='BannerFrame.TFrame')
bannerFrame.place(x=0, y=0)
bannerImageObject = Image.open("Images/banner.jpg").resize((250, 720))
bannerImage = ImageTk.PhotoImage(bannerImageObject)
Label(bannerFrame, image=bannerImage).place(x=0, y=0)

####-------------------------------------Taskbar------------------------------------------------
taskbarFrame = ttk.Frame(root, width=970, height=50, style='TaskbarFrame.TFrame')
taskbarFrame.place(x=280, y=20)

avatarImageObject = Image.open("Images/avatar.jpg").resize((40, 40))
avatarImage = ImageTk.PhotoImage(avatarImageObject)
Label(taskbarFrame, text='Menu', bg='#FFFFFF', fg='black', font=('Helvetica', 16, 'bold')).place(x=10, y=10)
avatarLabel = Label(taskbarFrame, image=avatarImage)
avatarLabel.place(x=500, y=3)
Label(taskbarFrame, text=UserData.username, bg='#FFFFFF', fg='black', font=('Helvetica', 16)).place(x=550, y=10)
signoutImageObject = Image.open("Images/signoutbutton.jpg").resize((30,30))
signoutImage = ImageTk.PhotoImage(signoutImageObject)
balance = get_balance()
balanceLabel = Label(taskbarFrame, text=f"Balance: {balance[0]}", bg='#FFFFFF', fg='black', font=('Helvetica', 16))
balanceLabel.place(x=700, y=10)
signoutButton = Button(taskbarFrame, image=signoutImage, bg='#FFFFFF', relief="flat", bd=0, command=sign_out)
signoutButton.place(x=900, y=10)

####-------------------------------------Menu------------------------------------------------
menuFrame = ttk.Frame(root, width=640, height=610, style='MenuFrame.TFrame')
menuFrame.place(x=280, y=90)

list_dish = get_menu()

photo_list = []

menuCanvas = tk.Canvas(menuFrame, width=615, height=607, bg='#FFFFFF')
menuCanvas.grid(row=0, column=0, sticky='NW')

scrollbar = ttk.Scrollbar(menuFrame, orient="vertical", command=menuCanvas.yview)
scrollbar.grid(row=0, column=1, sticky='NS')

menuCanvas.config(yscrollcommand=scrollbar.set)

displayDishFrame = ttk.Frame(menuCanvas, style='DisplayDishFrame.TFrame')
menuCanvas.create_window((0, 0), window=displayDishFrame, anchor='nw')

menuCanvas.bind('<Configure>', lambda e: menuCanvas.configure(scrollregion=menuCanvas.bbox("all")))

frame = ttk.Frame(menuCanvas)
menuCanvas.create_window((0, 0), window=frame, anchor="nw")

creat_widget_display_menu()

menuCanvas.bind("<MouseWheel>", update_scrollbar)
menuCanvas.bind('<Enter>', lambda e: menuCanvas.bind_all("<MouseWheel>", update_scrollbar))
menuCanvas.bind('<Leave>', lambda e: menuCanvas.bind_all("<MouseWheel>", reset_scrollbar))

####-------------------------------------Order------------------------------------------------
orderFrame = ttk.Frame(root, width=320, height=610, style='OrderFrame.TFrame')
orderFrame.place(x=940, y=90)
titleFrame = Frame(orderFrame, width=320, height=100, bg='#3366CC')
titleFrame.place(x=0, y=0)

Label(titleFrame, text='New Order', fg='#FFFFFF', bg='#3366CC', 
      font=('Helvetica', 20, 'bold')).place(x=10, y=30)
Label(titleFrame, text='Bàn: ', fg='#FFFFFF', bg='#3366CC', 
      font=('Helvetica', 16)).place(x=200, y=35)
tableSelect = Entry(titleFrame, bg='#3366CC', fg='#FFFFFF', width=3, font=('Helvetica', 15),
                    highlightthickness=0, bd=0)
tableSelect.place(x=250, y=35)
Frame(titleFrame, bg='#FFFFFF', height=2, width=90).place(x=200, y=60)

menuOrderFrame = ttk.Frame(orderFrame, width=300, height=360, style='MenuOrderFrame.TFrame')
menuOrderFrame.place(x=10, y=110)

order_columns = ('Name', 'Price')
treeOrder = ttk.Treeview(menuOrderFrame, columns=order_columns, show='headings', height=16)
treeOrder.column('Name', width=180)
treeOrder.column('Price', width=110)

txt = ttk.Scrollbar(menuOrderFrame, orient='vertical', command=treeOrder.yview)
txt.grid(row=0, column=1, sticky='NS')
treeOrder.configure(yscrollcommand=txt.set)
treeOrder.grid(row=0, column=0, sticky='NSEW')

Frame(orderFrame, bg='#000000', width=280, height=1).place(x=20, y=480)
Label(orderFrame, text='     Total:                       VNĐ     ', bg='#99FFFF', fg='#000000',
      font=('Helvetica', 16)).place(x=10, y=500)

totalAmount = 0
totalLabel = Label(orderFrame, text=totalAmount, bg='#99FFFF', fg='#000000', 
                   width=10, font=('Helvetica', 16), anchor='e')
totalLabel.place(x=100, y=500)

deleteDishButton = Button(orderFrame, text='Delete', bg='#00FFFF', fg='#000000',
                          font=('Helvetica', 14), cursor='hand2', relief="ridge", command=delete_dish)
deleteDishButton.place(x=10, y=550)
deleteAllDishButton = Button(orderFrame, text='Delete All', bg='#00FFFF', fg='#000000',
                             font=('Helvetica', 14), cursor='hand2', relief='ridge', command=delete_all_dish)
deleteAllDishButton.place(x=107, y=550)
orderButton = Button(orderFrame, text='Order', bg='#00FFFF', fg='#000000', width=6,
                     font=('Helvetica', 14), cursor='hand2', relief='ridge', command=order_dish)
orderButton.place(x=230, y=550)

####-------------------------------------END------------------------------------------------
root.mainloop()