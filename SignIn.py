from tkinter import *
from tkinter import messagebox
import pymysql
from UserData import UserData
from PIL import Image, ImageTk

# Tạo cửa sổ login
root = Tk()
root.title('Sign In')
root.geometry('925x500+300+150')
root.configure(bg = '#fff')
root.resizable(False, False) # ngăn chặn thay đổi kích thước cửa sổ
icon_path = "Images/icon.ico"
root.iconbitmap(icon_path)

def sign_in():
    global username
    username = user.get()
    UserData.username = username
    password = code.get()
    
    if username =='' and password == '':
        messagebox.showerror('Error', 'All Fields Are Required')
        
    elif username == 'admin' and password == '1111':
        root.destroy()
        import Admin
        
    else:
        try:
            conn = pymysql.connect(host='localhost', user='root', password='1111', database='manageorder')
            mycursor = conn.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Pleasr Try Again')
        
        query = 'select * from account where username=%s and password=%s'
        mycursor.execute(query, (user.get(), code.get()))
        result = mycursor.fetchone()
        if result == None:
            messagebox.showerror('Error', 'Invalid Username Or Password')
    
        else:
            root.destroy()
            import Customer
            
def signup_page():
    root.destroy()
    import SignUp

########----------------------------------------------------------------------------
# Chèn ảnh
img = PhotoImage(file='Images/gamerlogin.png')
Label(root, image=img, bg = 'white').place(x=80, y=10)

# Tạo khối login
frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

heading = Label(frame, text='Sign in', fg='#57a8f8', bg='white', font=('Tahoma', 23, 'bold'))
heading.place(x=120, y=10)

########----------------------------------------------------------------------------
# Ô nhập tài khoản
def on_enter(event):
    user.delete(0, 'end')

def on_leave(event):
    name = user.get()
    if name=='':
        user.insert(0, 'Username')

user = Entry(frame, width=30, fg='black', border=0, bg='white', font=('Tahoma', 14))
user.place(x=25, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=300, height=2, bg='black').place(x=25, y=107)

########----------------------------------------------------------------------------
# Ô nhập mật khẩu
def on_enter(event):
    if code.get() == 'Password':
        code.delete(0, 'end')
        code.config(show='*')

def on_leave(event):
    if code.get()=='':
        code.insert(0, 'Password')
        code.config(show='')

code = Entry(frame, width=30, fg='black', border=0, bg='white', font=('Tahoma', 14))
code.place(x=25, y=140)
code.insert(0, 'Password')
code.bind('<FocusIn>', lambda event: on_enter(code))
code.bind('<FocusOut>', lambda event: on_leave(code))

Frame(frame, width=295, height=2, bg='black').place(x=25, y=166)

########----------------------------------------------------------------------------
# Nút Sign In và Sign Up
Button(frame, width=39, pady=7, text="Sign in", bg='#57a8f8', fg='white', bd=0, cursor='hand2', command=sign_in).place(x=35, y=204)
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Tahoma', 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign Up', fg='#57a8f8', bd=0, bg='white', font=('Tahoma', 9), cursor='hand2', command=signup_page)
sign_up.place(x=215, y=270)

root.mainloop()