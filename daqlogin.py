from tkinter import Label, Button, Entry, Tk, StringVar
import tkMessageBox

mailids=list()
passwords=list()


def signincallback():
    global id, pwd
    id=entry1.get()
    pwd=entry2.get()
    if id != 'abcd' or pwd != '123':
        tkMessageBox.showerror("ERROR!", "Invalid Entry. Try again")
    #else:
        #code to open database


def signupcallback():
    mailids.append(entry1.get())
    passwords.append(entry2.get())
    #or write to a file

top = Tk()

top.title('Blood Pressure Monitoring System')
top.minsize(360,240)
top.maxsize(360,240)
top.configure(bg = 'lightgreen')


l1 = Label(top,text="E-mail")
l1.place(x=80,y=50)
entry1=StringVar()
entry1.set('Enter mail id here')
entrylabel1=Entry(top,textvariable=entry1,width=30)
entrylabel1.place(x=150,y=50)
l2 = Label(top,text="Password")
l2.place(x=80,y=100)
entry2=StringVar()
entrylabel2=Entry(top,textvariable=entry2,width=30)
entrylabel2.place(x=150,y=100)
b1 = Button(top,text="Sign in",command=signincallback)
b1.place(x=150,y=150)
b2 = Button(top,text="Sign up",command=signupcallback)
b2.place(x=200,y=150)


top.mainloop()