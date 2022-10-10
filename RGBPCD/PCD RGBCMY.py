from tkinter import *
from tkinter.tix import COLUMN
import PIL.Image
import PIL.ImageTk
from tkinter.filedialog import askopenfile

root = Tk()
root.title("Copy Image and Convert Image to RGBCMY")
root.geometry('+%d+%d'%(90,15))

canvas = Canvas(root, width=1200, height=650, bg="#c8c8c8")
canvas.grid(columnspan=4, rowspan=6)

original_label = Label(root, text="Citra Awal", font=("Futura Md BT", 27), bg="#c8c8c8", fg="#625252")
original_label.grid(column=0, row=1)
copy_label = Label(root, text="Hasil Copy", font=("Futura Md BT", 27), bg="#c8c8c8", fg="#625252")
copy_label.grid(column=1, row=1)
rgb_label = Label(root, text="Hasil Konversi Warna", font=("Futura Md BT", 27), bg="#c8c8c8", fg="#625252")
rgb_label.grid(column=2, row=1, columnspan=2)

#Create frame for layout
def frame():
    select = Frame(root, width=310, height=310)
    select.grid(column=0, row=2)
    copy = Frame(root, width=310, height=310)
    copy.grid(column=1, row=2)
    convert = Frame(root, width=310, height=310)
    convert.grid(column=2, row=2, columnspan=2)

frame()

#Select image function
def select_image():
    global img, image1
    select_img.set("loading...")
    img = askopenfile(parent=root, mode='rb', title='Choose an image', filetype=[("image file", "*.jpg"), ("image file", "*.png")])
    if img:
        image1 = PIL.Image.open(img)

        def resize_image(image1):
            width, height = int(image1.size[0]), int(image1.size[1])
            if width > height:
                height = int(300/width*height)
                width = 300
            elif height > width:
                width = int(250/height*width)
                height = 250
            else:
                width, height = 250, 250
            image1 = image1.resize((width, height))
            return image1

        def display_image(image1):
            global img_label
            image1 = resize_image(image1)
            image1 = PIL.ImageTk.PhotoImage(image1)
            img_label = Label(image=image1, bg="black")
            img_label.image = image1
            img_label.grid(column=0, row=2)
            return img_label

        display_image(image1)

    select_img.set("Select Image")

#Copy image function
def copy_image():
    global orig_pixel_map
    orig_pixel_map = image1.load()
    width, height = int(image1.size[0]), int(image1.size[1])

    image2 = PIL.Image.new('RGB', (width, height))
    new_pixel_map = image2.load()

    for x in range(width):
        for y in range(height):
            new_pixel_map[x, y] = orig_pixel_map[x, y]

    def resize_image(image2):
            width, height = int(image2.size[0]), int(image2.size[1])
            if width > height:
                height = int(300/width*height)
                width = 300
            elif height > width:
                width = int(250/height*width)
                height = 250
            else:
                width, height = 250, 250
            image2 = image2.resize((width, height))
            return image2

    def display_image(image2):
        global copy_label
        image2 = resize_image(image2)
        image2 = PIL.ImageTk.PhotoImage(image2)
        copy_label = Label(image=image2, bg="black")
        copy_label.image = image2
        copy_label.grid(column=1, row=2)
        return image2

    display_image(image2)

#Convert image to RGBCMY function
def convert(n):
    global image3
    width, height = int(image1.size[0]), int(image1.size[1])
    image3 = PIL.Image.new('RGB', (width, height))
    new_pixel_map2 = image3.load()

    #to convert image to R, G, B, C, M, Y
    for x in range(width):
        for y in range(height):
            orig_pixel = orig_pixel_map[x, y]
            orig_r = orig_pixel[0]
            orig_g = orig_pixel[1]
            orig_b = orig_pixel[2]

            new_r = orig_r
            new_g = orig_g
            new_b = orig_b
            new_pixel = (new_r, new_g, new_b)
            new_pixel_map2[x, y] = new_pixel

    image3 = PIL.Image.open(img).convert('RGB')

    r, g, b = image3.split()

    match n:
        case 1:
            r = r.point(lambda i: i * 1)
            g = g.point(lambda i: i * 0)
            b = b.point(lambda i: i * 0)
        case 2:
            r = r.point(lambda i: i * 0)
            g = g.point(lambda i: i * 1)
            b = b.point(lambda i: i * 0)
        case 3:
            r = r.point(lambda i: i * 0)
            g = g.point(lambda i: i * 0)
            b = b.point(lambda i: i * 1)
        case 4:
            r = r.point(lambda i: i * 0)
            g = g.point(lambda i: i * 1)
            b = b.point(lambda i: i * 1)
        case 5:
            r = r.point(lambda i: i * 1)
            g = g.point(lambda i: i * 0)
            b = b.point(lambda i: i * 1)
        case 6:
            r = r.point(lambda i: i * 1)
            g = g.point(lambda i: i * 1)
            b = b.point(lambda i: i * 0)

    image3 = PIL.Image.merge('RGB', (r, g, b))

    def resize_image(image3):
        width, height = int(image3.size[0]), int(image3.size[1])
        if width > height:
            height = int(300/width*height)
            width = 300
        elif height > width:
            width = int(250/height*width)
            height = 250
        else:
            width, height = 250, 250
        image3 = image3.resize((width, height))
        return image3

    def display_image(image3):
        global convert_label
        image3 = resize_image(image3)
        image3 = PIL.ImageTk.PhotoImage(image3)
        convert_label = Label(image=image3, bg="black")
        convert_label.image = image3
        convert_label.grid(column=2, row=2, columnspan=2)
        return image3
    
    display_image(image3)

#Reset function
def reset_images():
    frame()

#Buttons
select_img = StringVar()
select_btn = Button(root, textvariable=select_img, command=select_image, font='Tahoma', height=1, width=12)
select_img.set("Select Image")
select_btn.grid(column=0, row=3)

copy_img = StringVar()
copy_btn = Button(root, text="Copy Image", command=copy_image, font='Tahoma', height=1, width=12)
copy_btn.grid(column=1, row=3)

reset_btn = Button(root, text="Reset", command=reset_images, font='Tahoma', height=1, width=12)
reset_btn.grid(column=0, row=4)

red_btn = Button(root, text="RED", command=lambda:convert(1), font='Tahoma', fg='Red', height=1, width=9)
red_btn.grid(column=2, row=3)

green_btn = Button(root, text="GREEN", command=lambda:convert(2), font='Tahoma', fg='Green', height=1, width=9)
green_btn.grid(column=2, row=4)

blue_btn = Button(root, text="BLUE", command=lambda:convert(3), font='Tahoma', fg='Blue', height=1, width=9)
blue_btn.grid(column=2, row=5)

cyan_btn = Button(root, text="CYAN", command=lambda:convert(4), font='Tahoma', fg='Cyan', height=1, width=9)
cyan_btn.grid(column=3, row=3)

magenta_btn = Button(root, text="MAGENTA", command=lambda:convert(5), font='Tahoma', fg='Magenta', height=1, width=9)
magenta_btn.grid(column=3, row=4)

yellow_btn = Button(root, text="YELLOW", command=lambda:convert(6), font='Tahoma', fg='Yellow', height=1, width=9)
yellow_btn.grid(column=3, row=5)

root.mainloop()