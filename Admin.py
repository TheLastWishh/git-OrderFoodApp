import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
import random
from PIL import Image, ImageTk

root = Tk()
root.title('Manage')
root.geometry('1280x720+125+40')
root.resizable(False, False)
icon_path = "Images/icon.ico"
root.iconbitmap(icon_path)
tab_control = ttk.Notebook(root)

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

####--------------------------------HÀM QUẢN LÝ MENU MÓN ĂN----------------------------------------------
def get_data_dish():
    connect_serve()
    mycursor = conn.cursor()
    query = 'SELECT * FROM listdish'
    mycursor.execute(query)
    data = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return data

def ID_Dish(category):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        random_digits = ''
        for i in range(3):
            random_digits += str(random.choice(numbers))
        if category == 'FOOD':
            idDish = 'FO' + random_digits
        elif category == 'DRINK':
            idDish = 'DR' + random_digits
        return idDish

def set_data_dish_table():
    treeDish.delete(*treeDish.get_children())
    data = get_data_dish()
    for row in data:
        treeDish.insert('', 'end', values=row)

def add_dish():
    connect_serve()
    mycursor = conn.cursor()
    
    query = "SELECT * FROM listdish WHERE Name=%s"
    mycursor.execute(query, dishName.get())
    result = mycursor.fetchone()
    
    if result == None:
        cat = category.get()
        cat = cat.upper()
        if cat == 'FOOD' or cat == 'DRINK':
            if price.get().isdigit(): 
                id_dish = ID_Dish(cat)
                query = "INSERT INTO listdish() values (%s, %s, %s, %s)"
                mycursor.execute(query, (id_dish, dishName.get(), cat, price.get()))
                conn.commit()
                mycursor.close()
                conn.close()
                messagebox.showinfo('Notification', 'Added Successfully')
                set_data_dish_table()
            else:
                price.delete(0, END)
                messagebox.showerror('Error', 'Price Must Be A Number')
                mycursor.close()
                conn.close()
                return
        else:
            category.delete(0, END)
            mycursor.close()
            conn.close()
            messagebox.showerror('Error', 'Classifying Food Incorrectly')
            return
    else:
        dishName.delete(0, END)
        mycursor.close()
        conn.close()
        messagebox.showerror('Error', 'Dish Already Exists')
    
    dishName.delete(0, END)
    category.delete(0, END)
    price.delete(0, END)
        
def delete_dish():
    selected_dish = treeDish.selection()
    for dishID in selected_dish:
        connect_serve()
        mycursor = conn.cursor()
        dish_info = treeDish.item(dishID)
        query = "DELETE FROM listdish WHERE ID_Dish=%s"
        mycursor.execute(query, dish_info['values'][0])
        conn.commit()
        
        treeDish.delete(dishID)
        set_data_dish_table()
        messagebox.showinfo('Notification', 'Deleted Successfully')

def edit_dish():
    connect_serve()
    mycursor = conn.cursor()
    
    query = "SELECT * FROM listdish WHERE Name=%s"
    mycursor.execute(query, dishName.get())
    result = mycursor.fetchone()
    
    if result != None:
        cat = category.get()
        cat = cat.upper()
        if cat == 'FOOD' or cat == 'DRINK':
            if price.get().isdigit():
                id_dish = ID_Dish(cat)
                query = "UPDATE listdish SET ID_Dish=%s, Category=%s, Price=%s WHERE Name=%s"
                mycursor.execute(query, (id_dish, cat, price.get(), dishName.get()))
                conn.commit()
                mycursor.close()
                conn.close()
                messagebox.showinfo('Notification', 'Added Successfully')
                set_data_dish_table()
            else:
                price.delete(0, END)
                messagebox.showerror('Error', 'Price Must Be A Number')
                mycursor.close()
                conn.close()
                return
        else:
            category.delete(0, END)
            mycursor.close()
            conn.close()
            messagebox.showerror('Error', 'Classifying Food Incorrectly')
            return
    else:
        dishName.delete(0, END)
        mycursor.close()
        conn.close()
        messagebox.showerror('Error', 'Dish Not Exists')
    
    dishName.delete(0, END)
    category.delete(0, END)
    price.delete(0, END)

####-----------------------------HÀM QUẢN LÝ DANH SÁCH TÀI KHOẢN NGƯỜI DÙNG--------------------------------
def get_data_acc():
    connect_serve()
    mycursor = conn.cursor()
    query = 'SELECT * FROM account'
    mycursor.execute(query)
    data = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return data

def set_data_acc_table():
    treeAcc.delete(*treeAcc.get_children())
    data = get_data_acc()
    for row in data:
        treeAcc.insert('', 'end', values=row)

def del_acc():
    selected_acc = treeAcc.selection()
    for accID in selected_acc:
        connect_serve()
        mycursor = conn.cursor()
        acc_info = treeAcc.item(accID)
        query = "DELETE FROM account WHERE ID=%s"
        mycursor.execute(query, acc_info['values'][0])
        conn.commit()
        
        treeDish.delete(accID)
        set_data_acc_table()
        messagebox.showinfo('Notification', 'Deleted Successfully')
        mycursor.close()
        conn.close()

def edit_acc():
    connect_serve()
    mycursor = conn.cursor()
    
    query = "SELECT * FROM account WHERE Username=%s"
    mycursor.execute(query, usernameAcc.get())
    result = mycursor.fetchone()
    
    if result != None:
        query = "UPDATE account SET Password=%s WHERE Username=%s"
        mycursor.execute(query, (passwordAcc.get(), usernameAcc.get()))
        conn.commit()
        mycursor.close()
        conn.close()
        messagebox.showinfo('Notification', 'Password Changed Successfully')
        set_data_acc_table()
        usernameAcc.delete(0, END)
        passwordAcc.delete(0, END)
        depositAcc.delete(0, END)
    else:
        messagebox.showerror('Error', 'Dish Not Exists')
        usernameAcc.delete(0, END)
        passwordAcc.delete(0, END)
        depositAcc.delete(0, END)
        mycursor.close()
        conn.close()
        return
    
def deposit():
    connect_serve()
    mycursor = conn.cursor()
    
    query = "SELECT * FROM account WHERE Username=%s"
    mycursor.execute(query, usernameAcc.get())
    result = mycursor.fetchone()
    if result != None:
        if depositAcc.get().isdigit():
            query = "SELECT Balance FROM account WHERE Username=%s"
            mycursor.execute(query, usernameAcc.get())
            result = mycursor.fetchone()
            current_balance = int(result[0])
            added_balance = int(depositAcc.get()) + current_balance
            query = "UPDATE account SET Balance=%s WHERE Username=%s"
            mycursor.execute(query, (added_balance, usernameAcc.get()))
            conn.commit()
            mycursor.close()
            conn.close()
            messagebox.showinfo('Notification', 'Deposit Successfully')
            set_data_acc_table()
        else:
            depositAcc.delete(0, END)
            messagebox.showerror('Error', 'Money Must Be A Number')
            mycursor.close()
            conn.close()
    else:
        usernameAcc.delete(0, END)
        depositAcc.delete(0, END)
        messagebox.showerror('Error', 'Account Not Exists')
        mycursor.close()
        conn.close()

####------------------------------------HÀM QUẢN LÝ DANH SÁCH HÓA ĐƠN---------------------------------------
def get_data_bill():
    connect_serve()
    mycursor = conn.cursor()
    
    query = "SELECT * FROM bill ORDER BY OrderDate DESC"
    mycursor.execute(query)
    data = mycursor.fetchall()
    
    mycursor.close()
    conn.close()
    return data

def set_data_bill_table():
    treeBill.delete(*treeBill.get_children())
    data = get_data_bill()
    
    for row in data:
        treeBill.insert('', 'end', values=row)

def get_data_bill_detail(billID):
    connect_serve()
    mycursor = conn.cursor()
    
    query = '''
            SELECT bd.Name, bd.Quantity, ld.Price
            FROM BillDetail bd
            JOIN ListDish ld ON bd.Name = ld.Name
            WHERE bd.BillID = %s
    '''
    mycursor.execute(query, billID)
    
    result = mycursor.fetchall()
    bill_detail = []
    for row in result:
        name, quantity, price = row
        total_price = quantity * price
        bill_detail.append([name, quantity, total_price])
        
    return bill_detail

def set_data_bill_detail(billID):
    treeBillDetail.delete(*treeBillDetail.get_children())
    data = get_data_bill_detail(billID)
    
    for row in data:
        treeBillDetail.insert('', 'end', values=row)

def search_bill():
    connect_serve()
    mycursor = conn.cursor()
    
    if tableOrder.get() == '':
        query = "SELECT * FROM bill WHERE Username=%s ORDER BY OrderDate DESC"
        mycursor.execute(query, userOrder.get())
        data = mycursor.fetchall()
    else:
        query = "SELECT * FROM bill WHERE Username=%s and TableOrder=%s ORDER BY OrderDate DESC"
        mycursor.execute(query, (userOrder.get(), tableOrder.get()))
        data = mycursor.fetchall()
    
    treeBill.delete(*treeBill.get_children())
    
    for row in data:
        treeBill.insert('', 'end', values=row)
    
    mycursor.close()
    conn.close()

def refresh_bill():
    userOrder.delete(0, END)
    tableOrder.delete(0, END)
    billIDLabel.config(text=f"Bill ID: ")
    set_data_bill_table()
    int_var1.set('All')
    int_var2.set('All')
    treeBillDetail.delete(*treeBillDetail.get_children())

def pay_bill():
    selected_bill = treeBill.selection()
    for index in selected_bill:
        connect_serve()
        mycursor = conn.cursor()
        
        bill_info = treeBill.item(index, 'values')
        if bill_info[5] == 'unpaid':
            query = "UPDATE Bill SET PaymentStatus='Paid' WHERE BillID=%s"
            mycursor.execute(query, bill_info[0])
            conn.commit()
            mycursor.close()
            conn.close()
            messagebox.showinfo('Notification', 'Payment Success')
            
            updated_bill_info = list(bill_info)
            updated_bill_info[5] = 'paid'
            treeBill.item(index, values=updated_bill_info)
        else:
            messagebox.showinfo('Notification', 'This Bill Has Been Paid')

def complete_order():
    selected_bill = treeBill.selection()
    for index in selected_bill:
        connect_serve()
        mycursor = conn.cursor()
        
        bill_info = treeBill.item(index, 'values')
        if bill_info[6] == 'Preparing':
            query = "UPDATE Bill SET OrderStatus='Done' WHERE BillID=%s"
            mycursor.execute(query, bill_info[0])
            conn.commit()
            mycursor.close()
            conn.close()
            
            updated_bill_info = list(bill_info)
            updated_bill_info[6] = 'Done'
            treeBill.item(index, values=updated_bill_info)
        else:
            messagebox.showinfo('Notification', 'Order Has Been Served')

def detail_bill():
    select_bill = treeBill.selection()
    if len(select_bill) == 0:
        messagebox.showerror('Error', 'No Bill Are Selected')
    elif len(select_bill) == 1:
        bill_info = treeBill.item(select_bill, 'values')
        billIDLabel.config(text=f"Bill ID: {bill_info[0]}")
        set_data_bill_detail(bill_info[0])
    elif len(select_bill) >=2:
        messagebox.showerror('Error', 'Select Only 1 Bill')
    
def delete_bill():
    selected_bill = treeBill.selection()
    for index in selected_bill:
        connect_serve()
        mycursor = conn.cursor()
        
        bill_info = treeBill.item(index, 'values')
        query = "DELETE FROM BillDetail WHERE BillID=%s"
        mycursor.execute(query, bill_info[0])
        conn.commit()
       
        query = "DELETE FROM Bill WHERE BillID=%s"
        mycursor.execute(query, bill_info[0])
        conn.commit()
        mycursor.close()
        conn.close()
        
        treeBill.delete(index)

def paystatus_select(event):
    selected_value = paystatus_combobox.get()
    int_var2.set('All')
    if selected_value == 'All':
        set_data_bill_table()
    
    elif selected_value == 'Paid':
        treeBill.delete(*treeBill.get_children())
        connect_serve()
        mycursor = conn.cursor()
        query = 'SELECT * FROM bill WHERE PaymentStatus=%s'
        mycursor.execute(query, 'Paid')   
        result = mycursor.fetchall()
        for row in result:
            treeBill.insert('', 'end', values=row)      
        mycursor.close()
        conn.close()
    else:
        treeBill.delete(*treeBill.get_children())
        connect_serve()
        mycursor = conn.cursor()
        query = 'SELECT * FROM bill WHERE PaymentStatus=%s'
        mycursor.execute(query, 'Unpaid')
        result = mycursor.fetchall()
        for row in result:
            treeBill.insert('', 'end', values=row)
        mycursor.close()
        conn.close()

def orderstatus_select(event):
    selected_value = orderstatus_combobox.get()
    int_var1.set('All')
    
    if selected_value == 'All':
        set_data_bill_table()
    
    elif selected_value == 'Preparing':
        treeBill.delete(*treeBill.get_children())
        connect_serve()
        mycursor = conn.cursor()
        query = 'SELECT * FROM bill WHERE OrderStatus=%s'
        mycursor.execute(query, 'Preparing')   
        result = mycursor.fetchall()
        for row in result:
            treeBill.insert('', 'end', values=row)      
        mycursor.close()
        conn.close()
    else:
        treeBill.delete(*treeBill.get_children())
        connect_serve()
        mycursor = conn.cursor()
        query = 'SELECT * FROM bill WHERE OrderStatus=%s'
        mycursor.execute(query, 'Done')
        result = mycursor.fetchall()
        for row in result:
            treeBill.insert('', 'end', values=row)
        mycursor.close()
        conn.close()

####------------------------------------HÀM QUẢN LÝ DOANH THU----------------------------------------------
def get_list_bill_paid():
    month = months_combobox.get()
    year = years_combobox.get()
    
    if month == 'All' and year == 'All':
        connect_serve()
        mycursor = conn.cursor()
        
        query = '''
                SELECT BillID, TotalPrice, OrderDate
                FROM Bill
        '''
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        conn.close()
        return result
    
    elif month == 'All':
        connect_serve()
        mycursor = conn.cursor()
        
        query = '''
                SELECT BillID, TotalPrice, OrderDate
                FROM Bill
                WHERE Year(OrderDate)=%s
        '''
        mycursor.execute(query, year)
        result = mycursor.fetchall()
        mycursor.close()
        conn.close()
        return result
    elif year == 'All':
        connect_serve()
        mycursor = conn.cursor()
        
        query = '''
                SELECT BillID, TotalPrice, OrderDate
                FROM Bill
                WHERE Month(OrderDate)=%s
        '''
        mycursor.execute(query, month)
        result = mycursor.fetchall()
        mycursor.close()
        conn.close()
        return result
    else:
        connect_serve()
        mycursor = conn.cursor()
        
        query = '''
                SELECT BillID, TotalPrice, OrderDate
                FROM Bill
                WHERE Month(OrderDate)=%s and Year(OrderDate)=%s
        '''
        mycursor.execute(query, (month, year))
        result = mycursor.fetchall()
        mycursor.close()
        conn.close()
        return result

def cal_revenue():
    connect_serve()
    mycursor = conn.cursor()
    
    month = months_combobox.get()
    year = years_combobox.get()
    
    if month == 'All' and year == 'All':
        query = 'SELECT SUM(TotalPrice) FROM Bill'
        mycursor.execute(query)
        result = mycursor.fetchone()
        revenue.delete('0', 'end')
        revenue.insert(0, result)
    
    elif month == 'All':
        query = '''
                SELECT SUM(TotalPrice)
                FROM Bill
                WHERE Year(OrderDate)=%s
        '''
        mycursor.execute(query, year)
        result = mycursor.fetchone()
        revenue.delete('0', 'end')
        revenue.insert(0, result)
    
    elif year == 'All':
        query = '''
                SELECT SUM(TotalPrice)
                FROM Bill
                WHERE Month(OrderDate)=%s
        '''
        mycursor.execute(query, month)
        result = mycursor.fetchone()
        revenue.delete('0', 'end')
        revenue.insert(0, result)
    
    else:
        query = '''
                SELECT SUM(TotalPrice)
                FROM Bill
                WHERE Month(OrderDate)=%s AND Year(OrderDate)=%s
        '''
        mycursor.execute(query, (month, year))
        result = mycursor.fetchone()
        revenue.delete('0', 'end')
        revenue.insert(0, result)
    
    mycursor.close()
    conn.close()
    
def search_revenue():
    treeBillPaid.delete(*treeBillPaid.get_children())
    for col in bill_paid_columns:
        treeBillPaid.heading(col, text=col)
        
    list_bill = get_list_bill_paid()

    for row in list_bill:
        treeBillPaid.insert('', 'end', values=row)
        
    treeTopSales.delete(*treeTopSales.get_children())
    for col in top_sales_columns:
        treeTopSales.heading(col, text=col)

    list_top_sales = get_top_sales()

    for row in list_top_sales:
        treeTopSales.insert('', 'end', values=row)
        
    cal_revenue()
    
def get_top_sales():
    connect_serve()
    mycursor = conn.cursor()
    
    month = months_combobox.get()
    year = years_combobox.get()
    
    if month == 'All' and year == 'All':
        query = '''
            SELECT Name, Sum(Quantity) AS TotalSales
            FROM BillDetail
            GROUP BY Name
            ORDER BY TotalSales DESC
        '''
        mycursor.execute(query)
        result = mycursor.fetchall()
    
    elif month == 'All':
        query = '''
            SELECT bd.Name, SUM(bd.Quantity) AS TotalSales
            FROM BillDetail bd
            JOIN Bill b ON bd.BillID = b.BillID
            WHERE YEAR(b.OrderDate) = %s
            GROUP BY bd.Name
            ORDER BY TotalSales DESC;
        '''
        mycursor.execute(query, year)
        result = mycursor.fetchall()
    
    elif year == 'All':
        query = '''
            SELECT bd.Name, SUM(bd.Quantity) AS TotalSales
            FROM BillDetail bd
            JOIN Bill b ON bd.BillID = b.BillID
            WHERE MONTH(b.OrderDate) = %s
            GROUP BY bd.Name
            ORDER BY TotalSales DESC;
        '''
        mycursor.execute(query, month)
        result = mycursor.fetchall()
    
    else:
        query = '''
            SELECT bd.Name, SUM(bd.Quantity) AS TotalSales
            FROM BillDetail bd
            JOIN Bill b ON bd.BillID = b.BillID
            WHERE MONTH(b.OrderDate) = %s AND YEAR(b.OrderDate) = %s
            GROUP BY bd.Name
            ORDER BY TotalSales DESC;
        '''
        mycursor.execute(query, (month, year))
        result = mycursor.fetchall()
    
    mycursor.close()
    conn.close()
    return result

########---------------------------------------------------------------------------------------------------
s = ttk.Style()
s.configure('BannerFrame.TFrame', background='#3366CC')
s.configure("FoodTabFrame.TFrame", background='#DDDDDD')
s.configure("AccountTabFrame.TFrame", background='#DDDDDD')
s.configure("BillTabFrame.TFrame", background='#DDDDDD')
s.configure("RevenueTabFrame.TFrame", background='#DDDDDD')

########---------------------------------------------------------------------------------------------------
bannerImageObject = Image.open("Images/banner.jpg").resize((250, 720))
bannerImage = ImageTk.PhotoImage(bannerImageObject)
####--------------------------------QUẢN LÝ MENU MÓN ĂN----------------------------------------------
# Tab quản lý thực đơn
foodTab = ttk.Frame(tab_control)
tab_control.add(foodTab, text='    Dish Infomation    ')
tab_control.pack(expand=1, fill='both')

ttk.Frame(foodTab, width=1280, height=720, style='FoodTabFrame.TFrame').place(x=0, y=0)
bannerMenuFrame = ttk.Frame(foodTab, width=250, height=720, style='BannerFrame.TFrame')
bannerMenuFrame.place(x=0, y=0)
Label(bannerMenuFrame, image=bannerImage).place(x=0, y=0)

# Khu vực tùy chọn quản lý menu
optionFrame = Frame(foodTab, width=970, height=240, bg='#FFFFFF')
optionFrame.place(x=280, y=20)

Label(optionFrame, text='Option:', bg='#FFFFFF', font=('Helvetica', 20, 'bold')).place(x=40, y=20)
Frame(optionFrame, bg='#000000', width=120, height=2).place(x=40, y=50)


Label(optionFrame, text='Dish Name:', bg='#FFFFFF', font=('Helvetica', 16)).place(x=40, y=100)
dishName = Entry(optionFrame, bg='#FFFFFF', fg='#000000', width=16, font=('Helvetica', 15), bd=0)
dishName.place(x=160, y=100)
Frame(optionFrame, bg='#000000', width=180, height=2).place(x=160, y=125)

Label(optionFrame, text='Category:', bg='#FFFFFF', font=('Helvetica', 16)).place(x=360, y=100)
category = Entry(optionFrame, bg='#FFFFFF', fg='#000000', width=16, font=('Helvetica', 15), bd=0)
category.place(x=465, y=100)
Frame(optionFrame, bg='#000000', width=180, height=2).place(x=465, y=125)

Label(optionFrame, text='Price:', bg='#FFFFFF', font=('Helvetica', 16)).place(x=670, y=100)
price = Entry(optionFrame, bg='#FFFFFF', fg='#000000', width=16, font=('Helvetica', 15), bd=0)
price.place(x=750, y=100)
Frame(optionFrame, bg='#000000', width=180, height=2).place(x=750, y=125)

addButton = Button(optionFrame, text='Add Dish', bg='#00FFFF', fg='#000000', width=12,
                   font=('Helvetica', 14), cursor='hand2', relief='ridge', command=add_dish)
addButton.place(x=200, y=170)
delButton = Button(optionFrame, text='Delete Dish', bg='#00FFFF', fg='#000000', width=12,
                   font=('Helvetica', 14), cursor='hand2', relief='ridge', command=delete_dish)
delButton.place(x=400, y=170)
editButton = Button(optionFrame, text='Edit Dish', bg='#00FFFF', fg='#000000', width=12,
                   font=('Helvetica', 14), cursor='hand2', relief='ridge', command=edit_dish)
editButton.place(x=600, y=170)

# Danh sách menu
tableDish = Frame(foodTab, width=970, height=400, bg='#FFFFFF')
tableDish.place(x=280, y=280)

Label(tableDish, text='Menu', bg='#888888', 
      font=('Helvetica', 16, 'bold')).grid(column=0, row=0, columnspan=2, sticky='WE')

menu_columns = ('ID', 'Dish Name', 'Category', 'Price')
treeDish = ttk.Treeview(tableDish, columns=menu_columns, show='headings', height=17)
treeDish.column('ID', width=230)
treeDish.column('Dish Name', width=240)
treeDish.column('Category', width=240)
treeDish.column('Price', width=240)

for col in menu_columns:
    treeDish.heading(col, text=col)

set_data_dish_table()

txt = ttk.Scrollbar(tableDish, orient='vertical', command=treeDish.yview)
txt.grid(row=1, column=1, sticky='NS')
treeDish.configure(yscrollcommand=txt.set)
treeDish.grid(row=1, column=0, sticky='NSEW')

######------------------------------QUẢN LÝ TÀI KHOẢN CÁ NHÂN---------------------------------------
accountTab = ttk.Frame(tab_control)
tab_control.add(accountTab, text='    Account Information    ')
tab_control.pack(expand=1, fill='both')

ttk.Frame(accountTab, width=1280, height=720, style='AccountTabFrame.TFrame').place(x=0, y=0)
bannerAccFrame = ttk.Frame(accountTab, width=250, height=720, style='BannerFrame.TFrame')
bannerAccFrame.place(x=0, y=0)
Label(bannerAccFrame, image=bannerImage).place(x=0, y=0)

# Khu vực tùy chọn quản lý tài khoản
optionFrame = Frame(accountTab, width=970, height=240, bg='#FFFFFF')
optionFrame.place(x=280, y=20)

Label(optionFrame, text='Option:', bg='#FFFFFF', font=('Helvetica', 20, 'bold')).place(x=40, y=20)
Frame(optionFrame, bg='#000000', width=120, height=2).place(x=40, y=50)

Label(optionFrame, text='Username:', bg='#FFFFFF', font=('Helvetica', 16)).place(x=40, y=100)
usernameAcc = Entry(optionFrame, bg='#FFFFFF', fg='#000000', width=16, font=('Helvetica', 15), bd=0)
usernameAcc.place(x=160, y=100)
Frame(optionFrame, bg='#000000', width=180, height=2).place(x=160, y=125)

Label(optionFrame, text='Password:', bg='#FFFFFF', font=('Helvetica', 16)).place(x=360, y=100)
passwordAcc = Entry(optionFrame, bg='#FFFFFF', fg='#000000', width=16, font=('Helvetica', 15), bd=0)
passwordAcc.place(x=470, y=100)
Frame(optionFrame, bg='#000000', width=180, height=2).place(x=470, y=125)

Label(optionFrame, text='Deposit:', bg='#FFFFFF', font=('Helvetica', 16)).place(x=670, y=100)
depositAcc = Entry(optionFrame, bg='#FFFFFF', fg='#000000', width=16, font=('Helvetica', 15), bd=0)
depositAcc.place(x=765, y=100)
Frame(optionFrame, bg='#000000', width=180, height=2).place(x=765, y=125)

delButton = Button(optionFrame, text='Delete', bg='#00FFFF', fg='#000000', width=12,
                   font=('Helvetica', 14), cursor='hand2', relief='ridge', command=del_acc)
delButton.place(x=200, y=170)
editButton = Button(optionFrame, text='Edit', bg='#00FFFF', fg='#000000', width=12,
                   font=('Helvetica', 14), cursor='hand2', relief='ridge', command=edit_acc)
editButton.place(x=400, y=170)
depositButton = Button(optionFrame, text='Deposit', bg='#00FFFF', fg='#000000', width=12,
                   font=('Helvetica', 14), cursor='hand2', relief='ridge', command=deposit)
depositButton.place(x=600, y=170)

# Danh sách tài khoản cá nhân
tableAcc = Frame(accountTab, width=970, height=400, bg='#FFFFFF')
tableAcc.place(x=280, y=280)

Label(tableAcc, text='List Account', bg='#888888', 
      font=('Helvetica', 16, 'bold')).grid(column=0, row=0, columnspan=2, sticky='WE')

list_acc_columns = ('ID', 'Username', 'Password', 'Balance')
treeAcc = ttk.Treeview(tableAcc, columns=list_acc_columns, show='headings', height=17)
treeAcc.column('ID', width=230)
treeAcc.column('Username', width=240)
treeAcc.column('Password', width=240)
treeAcc.column('Balance', width=240)

for col in list_acc_columns:
    treeAcc.heading(col, text=col)

set_data_acc_table()

txt = ttk.Scrollbar(tableAcc, orient='vertical', command=treeAcc.yview)
txt.grid(row=1, column=1, sticky='NS')
treeAcc.configure(yscrollcommand=txt.set)
treeAcc.grid(row=1, column=0, sticky='NSEW')

######------------------------------------QUẢN LÝ HÓA ĐƠN--------------------------------------------
billTab = ttk.Frame(tab_control)
tab_control.add(billTab, text='    Bill Information    ')
tab_control.pack(expand=1, fill='both')

ttk.Frame(billTab, width=1280, height=720, style='BillTabFrame.TFrame').place(x=0, y=0)
bannerBillFrame = ttk.Frame(billTab, width=250, height=720, style='BannerFrame.TFrame')
bannerBillFrame.place(x=0, y=0)
Label(bannerBillFrame, image=bannerImage).place(x=0, y=0)

# Khu vực tùy chọn quản lý hóa đơn
optionFrame = Frame(billTab, width=970, height=240, bg='#FFFFFF')
optionFrame.place(x=280, y=20)

## Thanh toán hóa đơn
Label(optionFrame, text='Pay The Bill:', bg='#FFFFFF', font=('Helvetica', 18, 'bold')).place(x=40, y=10)
Frame(optionFrame, bg='#000000', width=190, height=2).place(x=40, y=40)

paybillFrame = Frame(optionFrame, bg='#FFFFFF', width=500, height=180, bd=1,
                     relief=tk.SOLID, highlightbackground="#00FF00")
paybillFrame.place(x=40, y=50)

Label(paybillFrame, text='Search', bg='#FFFFFF', font=('Helvetica', 14)).place(x=20, y=10)
Label(paybillFrame, text='User:', bg='#FFFFFF', font=('Helvetica', 14)).place(x=20, y=40)
userOrder = Entry(paybillFrame, bg='#FFFFFF', fg='#000000', width=13, font=('Helvetica', 13),
                  highlightthickness=0, bd=0)
userOrder.place(x=90, y=40)
Frame(paybillFrame, bg='#000000', width=120, height=2).place(x=90, y=60)

Label(paybillFrame, text='Table:', bg='#FFFFFF', font=('Helvetica', 14)).place(x=20, y=70)
tableOrder = Entry(paybillFrame, bg='#FFFFFF', fg='#000000', width=13, font=('Helvetica', 13),
                  highlightthickness=0, bd=0)
tableOrder.place(x=90, y=70)
Frame(paybillFrame, bg='#000000', width=120, height=2).place(x=90, y=90)

searchbillButton = Button(paybillFrame, text='Search', bg='#00FFFF', fg='#000000', width=8,
                          font=('Helvetica', 12), cursor='hand2', relief="ridge", command=search_bill)
searchbillButton.place(x=20, y=110)

Label(paybillFrame, text='Option', bg='#FFFFFF', font=('Helvetica', 14)).place(x=280, y=10)

payButton = Button(paybillFrame, text='Pay', bg='#00FFFF', fg='#000000', width=8,
                          font=('Helvetica', 12), cursor='hand2', relief="ridge", command=pay_bill)
payButton.place(x=280, y=55)

refreshButton = Button(paybillFrame, text='Refresh', bg='#00FFFF', fg='#000000', width=8,
                          font=('Helvetica', 12), cursor='hand2', relief="ridge", command=refresh_bill)
refreshButton.place(x=130, y=110)

doneButton = Button(paybillFrame, text='Complete', bg='#00FFFF', fg='#000000', width=8,
                          font=('Helvetica', 12), cursor='hand2', relief="ridge", command=complete_order)
doneButton.place(x=390, y=55)

detailButton = Button(paybillFrame, text='Detail', bg='#00FFFF', fg='#000000', width=8,
                          font=('Helvetica', 12), cursor='hand2', relief="ridge", command=detail_bill)
detailButton.place(x=280, y=110)

deleteButton = Button(paybillFrame, text='Delete', bg='#00FFFF', fg='#000000', width=8,
                          font=('Helvetica', 12), cursor='hand2', relief="ridge", command=delete_bill)
deleteButton.place(x=390, y=110)

## Tìm kiếm hóa đơn
Label(optionFrame, text='Search Bill:', bg='#FFFFFF', font=('Helvetica', 18, 'bold')).place(x=600, y=10)
Frame(optionFrame, bg='#000000', width=190, height=2).place(x=600, y=40)

Label(optionFrame, text='Payment Status', bg='#FFFFFF', font=('Helvetica', 14)).place(x=600, y=50)
int_var1 = StringVar()
int_var1.set('All')
paystatus_combobox = ttk.Combobox(optionFrame, textvariable=int_var1, values=['All', 'Paid', 'Unpaid'],
                               state='readonly', font=('Helvetica', 14))
paystatus_combobox.place(x=600, y=90)
paystatus_combobox.bind("<<ComboboxSelected>>", paystatus_select)

Label(optionFrame, text='Order Status', bg='#FFFFFF', font=('Helvetica', 14)).place(x=600, y=125)
int_var2 = StringVar()
int_var2.set('All')
orderstatus_combobox = ttk.Combobox(optionFrame, textvariable=int_var2, values=['All', 'Preparing', 'Done'],
                               state='readonly', font=('Helvetica', 14))
orderstatus_combobox.place(x=600, y=160)
orderstatus_combobox.bind("<<ComboboxSelected>>", orderstatus_select)

# Danh sách hóa đơn
tableBill = Frame(billTab, width=550, height=400, bg='#FFFFFF')
tableBill.place(x=280, y=280)

Label(tableBill, text='List Bill', bg='#888888', 
      font=('Helvetica', 16, 'bold')).grid(column=0, row=0, columnspan=2, sticky='WE')

list_bill_columns = ('BillID', 'Username', 'Order Date', 'Table', 'Total', 'Payment', 'Status')
treeBill = ttk.Treeview(tableBill, columns=list_bill_columns, show='headings', height=17)
treeBill.column('BillID', width=70)
treeBill.column('Username', width=100)
treeBill.column('Order Date', width=120)
treeBill.column('Table', width=45)
treeBill.column('Total', width=60)
treeBill.column('Payment', width=75)
treeBill.column('Status', width=75)

for col in list_bill_columns:
    treeBill.heading(col, text=col)

set_data_bill_table()

txt = ttk.Scrollbar(tableBill, orient='vertical', command=treeBill.yview)
txt.grid(row=1, column=1, sticky='NS')
treeBill.configure(yscrollcommand=txt.set)
treeBill.grid(row=1, column=0, sticky='NSEW')

# Chi tiết hóa đơn
tableBillDetail = Frame(billTab, width=390, height=400,  bg='#FFFFFF')
tableBillDetail.place(x=880, y=280)

billIDLabel = Label(tableBillDetail, text='Bill ID: ', bg='#888888', 
                    font=('Helvetica', 16, 'bold'))
billIDLabel.grid(row=0, column=0, columnspan=2, sticky='NSEW')

bill_detail_columns = ('Name', 'Quantity', 'Price')
treeBillDetail = ttk.Treeview(tableBillDetail, columns=bill_detail_columns, show='headings', height=17)
treeBillDetail.column('Name', width=150)
treeBillDetail.column('Quantity', width=100)
treeBillDetail.column('Price', width=100)

for col in bill_detail_columns:
    treeBillDetail.heading(col, text=col)
    
txt = ttk.Scrollbar(tableBillDetail, orient='vertical', command=treeBillDetail.yview)
txt.grid(row=1, column=1, sticky='NS')
treeBillDetail.configure(yscrollcommand=txt.set)
treeBillDetail.grid(row=1, column=0, sticky='NSEW')

######------------------------------------QUẢN LÝ DOANH THU------------------------------------------
revenueTab = ttk.Frame(tab_control)
tab_control.add(revenueTab, text='    Revenue Information    ')
tab_control.pack(expand=1, fill='both')

ttk.Frame(revenueTab, width=1280, height=720, style='RevenueTabFrame.TFrame').place(x=0, y=0)
bannerRevFrame = ttk.Frame(revenueTab, width=250, height=720, style='BannerFrame.TFrame')
bannerRevFrame.place(x=0, y=0)
Label(bannerRevFrame, image=bannerImage).place(x=0, y=0)

# Khu vực tùy chọn quản lý hóa đơn
optionFrame = Frame(revenueTab, width=970, height=240, bg='#FFFFFF')
optionFrame.place(x=280, y=20)

Label(optionFrame, text='Time:', bg='#FFFFFF', font=('Helvetica', 20, 'bold')).place(x=40, y=20)
Frame(optionFrame, bg='#000000', width=120, height=2).place(x=40, y=50)

filter1_var = StringVar()
filter1_var.set('All')
list_months = ['All', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
Label(optionFrame, text='Month:', bg='#FFFFFF', width=8,
      font=('Helvetica', 16), anchor='w').place(x=40, y=80)
months_combobox = ttk.Combobox(optionFrame, textvariable=filter1_var, values=list_months,
                               state='readonly', font=('Helvetica', 16), width=10)
months_combobox.place(x=150, y=80)

filter2_var = StringVar()
filter2_var.set('All')
Label(optionFrame, text='Year:', bg='#FFFFFF', width=8,
      font=('Helvetica', 16), anchor='w').place(x=320, y=80)
list_years = ['All', '2023', '2024']
years_combobox = ttk.Combobox(optionFrame, textvariable=filter2_var, values=list_years,
                               state='readonly', font=('Bookman Bold', 14), width=10)
years_combobox.place(x=420, y=80)

searchRevenueButton = Button(optionFrame, text='Search', 
                            width=15, pady=0, fg='black', bg='#FFFFFF', font=('Times New Roman', 11), 
                            relief='sunken', cursor='hand2', command=search_revenue)
searchRevenueButton.place(x=240, y=150)

revenueFrame = Frame(optionFrame, bg='#FFFFFF', width=240, height=180, bd=1,
                     relief=tk.SOLID, highlightbackground="#00FF00")
revenueFrame.place(x=660, y=30)

Label(revenueFrame, text='Revenue:', bg='#FFFFFF', font=('Helvetica', 20, 'bold')).place(x=40, y=20)
revenue = Entry(revenueFrame, bg='#FFFFFF', width=12, font=('Helvetica', 20, 'bold'), bd=1,
                     relief=tk.SOLID, highlightbackground="#00FF00")
revenue.place(x=40, y=80)
cal_revenue()

# Danh sách hóa đơn đã thanh toán
tableBillPaid = Frame(revenueTab, width=550, height=400, bg='#FFFFFF')
tableBillPaid.place(x=280, y=280)

Label(tableBillPaid, text='List Of Paid Bill', bg='#888888', 
      font=('Helvetica', 16, 'bold')).grid(column=0, row=0, columnspan=3, sticky='WE')

bill_paid_columns = ('BillID', 'TotalAmount', 'Sale Date')
treeBillPaid = ttk.Treeview(tableBillPaid, columns=bill_paid_columns, show='headings', height=17)
treeBillPaid.column('BillID', width=175)
treeBillPaid.column('TotalAmount', width=175)
treeBillPaid.column('Sale Date', width=175)


for col in bill_paid_columns:
    treeBillPaid.heading(col, text=col)

list_bill_paid = get_list_bill_paid()

for row in list_bill_paid:
    treeBillPaid.insert('', 'end', values=row)

txt = ttk.Scrollbar(tableBillPaid, orient='vertical', command=treeBillPaid.yview)
txt.grid(row=1, column=1, sticky='NS')
treeBillPaid.configure(yscrollcommand=txt.set)
treeBillPaid.grid(row=1, column=0, sticky='NSEW')

# Top món ăn được bán nhiều nhất
tableTopSales = Frame(revenueTab, width=390, height=400,  bg='#FFFFFF')
tableTopSales.place(x=880, y=280)

Label(tableTopSales, text='Bill ID: ', bg='#888888', 
                    font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, sticky='NSEW')

top_sales_columns = ('Name', 'Totalsales')
treeTopSales = ttk.Treeview(tableTopSales, columns=top_sales_columns, show='headings', height=17)
treeTopSales.column('Name', width=175)
treeTopSales.column('Totalsales', width=175)

for col in top_sales_columns:
    treeTopSales.heading(col, text=col)

list_top_sales = get_top_sales()

for row in list_top_sales:
    treeTopSales.insert('', 'end', values=row)

txt = ttk.Scrollbar(tableTopSales, orient='vertical', command=treeTopSales.yview)
txt.grid(row=1, column=1, sticky='NS')
treeTopSales.configure(yscrollcommand=txt.set)
treeTopSales.grid(row=1, column=0, sticky='NSEW')
######-----------------------------------------KẾT THÚC----------------------------------------------

root.mainloop()