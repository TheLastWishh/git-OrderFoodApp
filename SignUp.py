from tkinter import *
from tkinter import messagebox
import pymysql

###############--------------------------------------------------------------------------------------
def login_page():
    root.destroy()
    import SignIn

def connect_database():
    if username.get() == 'Username' or password.get() == 'Password' or confirm.get() == 'Confirm Password':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif password.get() != confirm.get():
        messagebox.showerror('Error', 'Password Mismatch')
        
    elif check.get() == 0:
        messagebox.showerror('Error', 'Please Accept Terms & Conditions')
        
    else:
        try:
            conn = pymysql.connect(host='localhost', user='root', password='1111', database='manageorder')
            mycursor = conn.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Pleasr Try Again')
            return
        
        query = 'select * from account where username=%s'
        mycursor.execute(query, (username.get()))
        result = mycursor.fetchone()
        if result != None:
            messagebox.showerror('Error', 'Username Already Exists')
        else:
            mycursor.execute("SELECT generate_account_id()")
            result = mycursor.fetchone()
            generated_id = result[0]
            query = 'insert into account(id , username, password) values (%s,%s,%s)'
            mycursor.execute(query, (generated_id, username.get(), password.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Registration is successfull')
            login_page()   
        
###############--------------------------------------------------------------------------------------
root = Tk()
root.title('Sign Up')
root.geometry('925x500+300+150')
root.configure(bg='white')
root.resizable(False, False)
icon_path = "Images/icon.ico"
root.iconbitmap(icon_path)

img = PhotoImage(file='Images/gamerlogin.png')
Label(root, image=img, bg='white').place(x=80, y=10)

frame = Frame(root, width='350', height='420', bg='white')
frame.place(x=480, y=40)

heading = Label(frame, text='Sign Up', fg='#57a8f8', bg='white', font=('Roboto', 28, 'bold'))
heading.place(x=110, y=30)

###############--------------------------------------------------------------------------------------
def on_enter(event):
    username.delete(0, 'end')
    
def on_leave(event):
    name = username.get()
    if name == '':
        username.insert(0, 'Username')

username = Entry(frame, width=28, fg='black', border=0, bg='white', font=('Roboto', 14))
username.place(x=25, y=110)
username.insert(0, 'Username')
username.bind('<FocusIn>', on_enter)
username.bind('<FocusOut>', on_leave)

Frame(frame, width=280, height=2,  bg='black').place(x=25, y=135)
###############--------------------------------------------------------------------------------------
def on_enter_password(event):
    if password.get() == 'Password':
        password.delete(0, 'end')
        password.config(show='*')
        
def on_leave_password(event):
    if password.get() == '':
        password.insert(0, 'Password')
        password.config(show='')

password = Entry(frame, width=28, fg='black', border=0, bg='white', font=('Roboto', 14))
password.place(x=25, y=160)
password.insert(0, 'Password')
password.bind('<FocusIn>', on_enter_password)
password.bind('<FocusOut>', on_leave_password)

Frame(frame, width=280, height=2,  bg='black').place(x=25, y=185)

###############--------------------------------------------------------------------------------------
def on_enter_confirm(event):
    if confirm.get() == 'Confirm Password':
        confirm.delete(0, 'end')
        confirm.config(show='*')

def on_leave_confirm(event):
    if confirm.get() == '':
        confirm.insert(0, 'Confirm Password')
        confirm.config(show='')

confirm = Entry(frame, width=28, fg='black', border=0, bg='white', font=('Roboto', 14))
confirm.place(x=25, y=215)
confirm.insert(0, 'Confirm Password')
confirm.bind('<FocusIn>', on_enter_confirm)
confirm.bind('<FocusOut>', on_leave_confirm)

Frame(frame, width=280, height=2, bg='black').place(x=25, y=240)
###############--------------------------------------------------------------------------------------
check = IntVar()
termsandcondition = Checkbutton(frame, text='I agree to the Terms & Conditions', fg='black', bg='white', font=('Roboto', 10), variable=check)
termsandcondition.place(x=25, y=260)

signupButton = Button(frame, width=27, text='Sign Up', bg='#57a8f8', fg='white', bd=0, cursor='hand2', font=('Roboto', 15), command=connect_database)
signupButton.place(x=25, y=300)

label = Label(frame, text="I have an account", fg='black', bg='white', font=('Roboto', 10))
label.place(x=75, y=360)

signinButton = Button(frame, width=6, text='Sign In', fg='#57a8f8', bd=0, bg='white', font=('Tahoma', 9), cursor='hand2', command=login_page)
signinButton.place(x=190, y=360)

root.mainloop()