from ctypes.wintypes import RGB
from tkinter import *
import tkinter as tk
from turtle import right
from PIL import Image
import PIL.Image
from PIL import ImageTk
import tkinter.filedialog
from array import *
from tkinter import simpledialog
from matplotlib import image
from matplotlib.offsetbox import TextArea
from matplotlib.pyplot import fill, gray
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.scrolledtext as st
import numpy as np

root = Tk()
root.title("Convert Image to Grayscale and Image Manipulation")
#root.geometry('+%d+%d'%(90,15))

canvas = Canvas(root, width=1200, height=650, bg="#c8c8c8")
canvas.grid(columnspan=4, rowspan=7)


#mengatur label atau tulisan statis
original_label = Label(root, text="Citra Awal", font=("Futura Md BT", 20), bg="#c8c8c8", fg="#625252")
original_label.grid(column=0, row=1)
grayscale_label = Label(root, text="Hasil Konversi Grayscale", font=("Futura Md BT", 20), bg="#c8c8c8", fg="#625252")
grayscale_label.grid(column=1, row=1)
brightness_label = Label(root, text="Mengatur Brightness", font=("Futura Md BT", 20), bg="#c8c8c8", fg="#625252")
brightness_label.grid(column=2, row=1)
negasi_label = Label(root, text="Hasil Negasi", font=("Futura Md BT", 20), bg="#c8c8c8", fg="#625252")
negasi_label.grid(column=3, row=1)


#mengatus function untuk mengambil  pixel
def pixel(pics):
    global arr, arr_text, arr_gray
    
    x = 0
    y = 0
    arr = []
    arr_text = []
    arr_gray = []
    
    for i in range(w):
        for j in range(h):
            rvalue = pics.getpixel((x,y))[0]
            gvalue = pics.getpixel((x,y))[1]
            bvalue = pics.getpixel((x,y))[2]
            arr.append([x, y, rvalue, gvalue, bvalue])
            arr_text.append([rvalue])
            arr_gray.append([x, y, rvalue])
            j += 1
            y += 1
        x += 1
        i += 1
        y = 0
        j = 0 

#Create frame for layout
def frame():
    #definisikan bagian select
    select = Frame(root, width=250, height=250)
    select.grid(column=0, row=2)
    
    #definisikan bagian grayscale
    grayscale = Frame(root, width=250, height=250)
    grayscale.grid(column=1, row=2)
    
    #definisikan bagian brightness
    brightness = Frame(root, width=250, height=250)
    brightness.grid(column=2, row=2)
    
    #definisikan bagian negasi
    negasi = Frame(root, width=250, height=250)
    negasi.grid(column=3, row=2)

#mendefinisikan fungsi untuk membuka file
def open_file():
    global w, h, pics
    
    #menggunakan fungsi tkinter.filedialog.askopenfilename() untuk mengambil judul dari file yang dipilih
    file_path = tkinter.filedialog.askopenfilename()
    
    #dengan alamat file sebelumnya, kita gunakan fungsi dari PIL untuk membuka file tersebut
    pics = (PIL.Image.open(file_path))
    
    #mengubah mode warna menjadi RGB
    pics = pics.convert('RGB')
    
    sizing = pics.resize((204,204))
    photo = PIL.ImageTk.PhotoImage(sizing)
    my_label = Label(image=photo)
    my_label.image = photo
    my_label.grid(row= 2, column= 0, pady= 2)
    
    w, h = pics.size

#mendefinisikan fungsi untuk grayscale
def grayscale():
    global ubah
    
    size = w,h
    
    pixel(pics)
    
    #membuat gambar baru dengan mode RGD dengan ukuran sesuai variabel size
    ubah = PIL.Image.new('RGB', size)
    load = ubah.load()
    
    for cr in arr:
        x, y, rvalue, gvalue, bvalue = cr
        
        #menghitung nilai grayscale dengan rumus
        gray = (rvalue + gvalue + bvalue)//3
        
        load[x,y] = (gray, gray, gray)
    
        sizing = ubah.resize((204,204))
    photo = PIL.ImageTk.PhotoImage(sizing)
    my_label = Label(image=photo)
    my_label.image = photo        
    my_label.grid(row= 2, column= 1, pady= 2)
    
    TextArea.delete(1.0, END)
    pixel(ubah)
    TextArea.insert(tk.INSERT, arr_text)

def brightadj():
    size = w,h
    
    pixel(ubah)
    
    input = simpledialog.askinteger(title="Input", prompt="Nilai Peningkatan")
        
    pics3 = PIL.Image.new('RGB', size)
    load = pics3.load()
    
    for cr in arr_gray:
        x, y, gray = cr  
        adj = gray + input
        load[x,y] = (adj, adj, adj)
    
    sizing = pics3.resize((204,204))
    photo = PIL.ImageTk.PhotoImage(sizing)
    my_label = Label(image=photo)
    my_label.image = photo
    my_label.grid(row= 2, column= 2)
    
    TextArea2.delete(1.0, END)
    pixel(pics3)
    TextArea2.insert(tk.INSERT, arr_text)
    
def negasi():
    size = w, h
    
    pixel(ubah)
        
    pics4 = PIL.Image.new('RGB', size)
    load = pics4.load()

    for cr in arr_gray:
        x, y, gray = cr
        ntn = 255 - gray
        load[x,y] = (ntn, ntn, ntn)
    
    sizing = pics4.resize((204,204))
    photo = PIL.ImageTk.PhotoImage(sizing)
    my_label = Label(image=photo)
    my_label.image = photo
    my_label.grid(row= 2, column= 3, pady= 2)
    
    TextArea2.delete(1.0, END)
    pixel(pics4)
    TextArea2.insert(tk.INSERT, arr_text)
       
frame()

#definisikan button select image
select_btn = Button(root, text="Select Image", font='Tahoma', command=open_file, height=1, width=12)
#select_img.set("Select Image")
select_btn.grid(column=0, row=3)


#definisikan button grayscale
gray_img = StringVar()
gray_btn = Button(root, text="Grayscale", font='Tahoma', command=grayscale, height=1, width=12)
gray_btn.grid(column=1, row=3)

bright_btn = Button(root, text="Brightness", font='Tahoma', command=brightadj, height=1, width=9)
bright_btn.grid(column=2, row=3)

negasi_btn = Button(root, text="Negasi", font='Tahoma', command=negasi, height=1, width=9)
negasi_btn.grid(column=3, row=3)

reset_btn = Button(root, text="Reset", font='Tahoma', height=1, width=12)
reset_btn.grid(column=0, row=4)

root.mainloop()