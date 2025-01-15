from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image,ImageTk
import os
from stegano import lsb
from pvd import hide_pvd,reveal_pvd
from MatrixEmbedding import encode_matrix_embedding, decode_matrix_embedding
import time

root = Tk()
root.title("Stegano hidden message")
root.geometry("700x500+150+180")
root.resizable(False,False)
root.configure(bg="#2f4155")


def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select Image File",
                                          filetypes=(("PNG file", "*.png"),
                                                     ("JPG file", "*.jpg"),
                                                     ("ALL files", "*.*")))
    
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img, width=250, height=250)
    lbl.image = img

def hide():
    global secret
    message=text1.get(1.0,END)
  
    selected_option = option_var.get()
    if selected_option == "LSB":
        start_time = time.time()
        secret = lsb.hide(str(filename), message)
        end_time = time.time()
        print(f"Time taken for LSB: {end_time - start_time} seconds")
    elif selected_option == "PVD":
        start_time = time.time()
        secret = hide_pvd(str(filename), message)
        end_time = time.time()
        print(f"Time taken for PVD: {end_time - start_time} seconds")
    elif selected_option == "Matrix":
        start_time = time.time()
        secret = encode_matrix_embedding(str(filename), message)
        end_time = time.time()
        print(f"Time taken for Matrix: {end_time - start_time} seconds")

def show():
    selected_option = option_var.get()
    start_time = time.time()
    
    if selected_option == "LSB":
        clear_message = lsb.reveal(filename)
    elif selected_option == "PVD":
        clear_message = reveal_pvd(filename)
    elif selected_option == "Matrix":
        clear_message = decode_matrix_embedding(filename)
    end_time = time.time()
    print(f"Time taken for show {selected_option}: {end_time - start_time} seconds")

    text1.delete(1.0, END)
    text1.insert(END, clear_message)
        
def save():
    #save base on option
    selected_option = option_var.get()
    if selected_option == "LSB":
        secret.save("LSB_hidden.png")
    elif selected_option == "PVD":
        secret.save("PVD_hidden.png")
    elif selected_option == "Matrix":
        secret.save("Matrix_hidden.png")
    
image_icon=PhotoImage(file="logoscre.jpg")
root.iconphoto(False,image_icon)

logo =PhotoImage(file="logoscre.png")
Label(root,image=logo,bg="#2f4155").place(x=10,y=0)

Label(root,text="CYBER SCIENE",bg="#2f4155",fg="white",font="arial 25 bold").place(x=100,y=20)

f=Frame(root,bd=3,bg="black",width=340,height=280,relief=GROOVE)
f.place(x=10,y=80)

lbl=Label(f,bg="black")
lbl.place(x=40,y=10)

f2=Frame(root,bd=3,bg="white",width=340,height=280,relief=GROOVE)
f2.place(x=350,y=80)

text1=Text(f2,font="Robote 20",bg="white",fg="black",relief=GROOVE)
text1.place(x=0,y=0,width=320,height=295)

scrollbar1=Scrollbar(f2)
scrollbar1.place(x=320,y=0,height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

f3=Frame(root,bd=3,bg="#2f4155",width=330,height=100,relief=GROOVE)
f3.place(x=10,y=370)

Button(f3,text="Open Image",width=10,height=2,font="arial 14 bold",command=showimage).place(x=20,y=30)
Button(f3,text="Save Image",width=10,height=2,font="arial 14 bold",command=save).place(x=180,y=30)
Label(f3,text="Picture,Image,Photofile",bg="#2f4155",fg="yellow").place(x=20,y=5)

f4=Frame(root,bd=3,bg="#2f4155",width=330,height=100,relief=GROOVE)
f4.place(x=360,y=370)

option_var = StringVar(root)
option_var.set("LSB")  # Default value

options = ["LSB", "PVD", "Matrix"]  # Add more options as needed
option_menu = OptionMenu(f4, option_var, *options)
option_menu.place(x=250, y=10)

Button(f4,text="Hide Data",width=8,height=1,font="arial 14 bold",command=hide).place(x=20,y=50)
Button(f4,text="Show Data",width=8,height=1,font="arial 14 bold",command=show).place(x=180,y=50)
Label(f4,text="Picture,Image,Photofile",bg="#2f4155",fg="yellow").place(x=20,y=5)



root.mainloop()