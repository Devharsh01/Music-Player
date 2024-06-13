from tkinter import *
from moviepy.decorators import audio_video_fx
from mutagen.mp3 import MP3
from tkinter import ttk
import time
from PIL import Image
from tkinter import filedialog
import PIL.ImageTk as ImageTk
import pygame
import os

root = Tk()
root.title("MP3 Player")
root.geometry("550x500+30+30")

pygame.mixer.init()

def volume_func(e):
    #This takes a float value between 0 and 1
    a = abs(1-(volume.get()))
    pygame.mixer.music.set_volume(a)

def add_song():
    global box,songs
    file = filedialog.askopenfilenames(initialdir="F:\Songs",title="Add Songs",filetypes=(("MP3 Files","*.mp3"),("MP4 Files","*.mp4"),("All Files","*.*")))
    for i in file:
        songs.append(i)
        s = i[::-1]
        a = s.index('/')
        i = i[-(a):]
        a = s.index('.')
        i = i[:-(a+1)]
        box.insert(END, i)

def time_show():
    global songs,box,paused,Time,total_time,length,shift
    a = box.curselection()
    if shift == False and a:
        taken = pygame.mixer.music.get_pos()
        taken = int(taken/1000)
        length.config(value=taken)
        taken = time.strftime("%M:%S",time.gmtime(taken))
        Time.config(text=taken + " of " + str(total_time))
        Time.after(1000,time_show)

def start():
    global box,songs,paused,play_img,pause_img,temp,total_time,shift,volume,count
    song = box.get(ACTIVE) 
    a = box.curselection()
    if song != temp:
        paused = "True0"
        temp = song
    final = ""
    x = ""
    for i in songs:
        if song in i:
            final = i
            break
    if paused == "True0" and a:
        pygame.mixer.music.load(final)
        pygame.mixer.music.play(loops=0)
        count = 0
        length['state'] = NORMAL
        paused = "False1"
        play.config(image=pause_img)
        shift = False
        x = MP3(final)
        total_time = int(x.info.length)
        length.config(to=total_time)
        total_time = time.strftime("%M:%S",time.gmtime(total_time))
        volume['state'] = NORMAL
        time_show()
    elif paused == "True1" and shift :
        pygame.mixer.music.unpause()
        paused = "False1"
        volume['state'] = NORMAL
        play.config(image=pause_img)
        reset()
    elif paused == "True1":
        pygame.mixer.music.unpause()
        paused = "False1"
        volume['state'] = NORMAL
        play.config(image=pause_img)
        time_show()
    elif paused == "False1":
        pygame.mixer.music.pause()
        paused = "True1"
        play.config(image=play_img)

def stopped():
    global play_img,pause_img,paused,shift,count
    count = 0
    pygame.mixer.music.stop()
    box.selection_clear(0,END)
    Time.config(text="")
    length.config(value=0)
    length['state']=DISABLED
    volume['state'] = DISABLED
    volume.config(value=0)
    paused = "True0"
    shift = False
    play.config(image=play_img)
    box.activate(-1)

def add_folder():
    global box,songs
    file = filedialog.askdirectory(initialdir="D:\Songs",title="Add Folder")
    if file:
        a = (os.listdir(file))
        for i in a:
            s = str(file)+"/"+i
            a = i.index('.')
            i = i[:a]
            box.insert(END, i)
            songs.append(s)

def del_song():
    box.delete(ANCHOR)
    stopped()

def del_all():
    box.delete(0,END)
    stopped()

def forward_():
    global box,songs,paused,play_img,pause_img,temp,shift,count
    song = box.get(ACTIVE)
    count = 0
    final = ""
    for i in songs:
        if song in i:
            final = songs.index(i)
            break
    if final != len(songs)-1:
        x = box.curselection()
        box.selection_clear(0,END)
        x = x[0] + 1
        box.activate(x)
        box.selection_set(x, last= None)
        paused = "True0"
        shift = False
        start()

def back():
    global box,songs,paused,play_img,pause_img,temp,shift,count
    count = 0
    song = box.get(ACTIVE)
    final = ""
    for i in songs:
        if song in i:
            final = songs.index(i)
            break
    if final != 0:
        x = box.curselection()
        box.selection_clear(0,END)
        x = x[0] - 1
        box.activate(x)
        box.selection_set(x, last= None)
        paused = "True0"
        shift = False
        start()

def again():
    global box,songs,shift,count
    song = box.get(ACTIVE)
    count = 0
    final = ""
    for i in songs:
        if song in i:
            final = songs.index(i)
            break
    a = box.curselection()
    shift = False
    if a:
        pygame.mixer.music.load(songs[final])
        pygame.mixer.music.play(loops=0)
        volume['state'] = NORMAL
        time_show()

def reset():
    global songs,box,length,Time,paused,total_time
    b = box.curselection()
    if shift and b and paused=="False1":
        a = int(length.get())
        a = a + 1 
        length.config(value=a)
        taken = time.strftime("%M:%S",time.gmtime(int(length.get())))
        Time.config(text=taken + " of " + str(total_time))
        Time.after(1000,reset)

def adjust(e):
    global songs,box,length,Time,paused,total_time,shift,count
    song = box.get(ACTIVE) 
    final = ""
    for i in songs:
        if song in i:
            final = i
            break
    pygame.mixer.music.load(final)
    pygame.mixer.music.play(loops=0,start=int(length.get()))
    volume['state'] = NORMAL
    length.config(value=int(length.get()))
    taken = time.strftime("%M:%S",time.gmtime(int(length.get())))
    Time.config(text=taken + " of " + str(total_time))
    shift = True
    count+=1
    if count == 1:
        Time.after(1000,reset)

songs=[]
paused = "True0"
temp = ""
count = 0
total_time = 0
shift = False

main_frame = Frame(root)
main_frame.pack(pady=10)

box = Listbox(main_frame,bg="black",fg="light blue",width=70,height=15,selectbackground="light blue",selectforeground="green")
box.grid(row=0,column=0,pady=10)

frame = Frame(main_frame)
frame.grid(row=1,column=0,pady=10)

backward_img = ImageTk.PhotoImage(Image.open("D:\Program Photos\Backward.png"))
forward_img = ImageTk.PhotoImage(Image.open("D:\Program Photos\Forward.png"))
pause_img = ImageTk.PhotoImage(Image.open("D:\Program Photos\Pause.png"))
play_img = ImageTk.PhotoImage(Image.open("D:\Program Photos\Play.png"))
repeat_img = ImageTk.PhotoImage(Image.open("D:\Program Photos\Repeat.png"))
stop_img = ImageTk.PhotoImage(Image.open("D:\Program Photos\Stop.png"))

backward = Button(frame,image=backward_img,command=back)
repeat = Button(frame,image=repeat_img,command=again)
play = Button(frame,image=play_img,command=start)
stop = Button(frame,image=stop_img,command=stopped)
forward = Button(frame,image=forward_img,command=forward_)

backward.grid(row=0,column=0,padx=10)
repeat.grid(row=0,column=1,padx=10)
play.grid(row=0,column=2,padx=10)
stop.grid(row=0,column=3,padx=10)
forward.grid(row=0,column=4,padx=10)

my_menu = Menu(root)
root.config(menu=my_menu)

add_menu = Menu(my_menu,tearoff="off")
my_menu.add_cascade(label="Add Songs",menu=add_menu)
add_menu.add_command(label="Add Songs",command=add_song)
add_menu.add_command(label="Add Folder",command=add_folder)

delete_menu = Menu(my_menu,tearoff="off")
my_menu.add_cascade(label="Delete Songs",menu=delete_menu)
delete_menu.add_command(label="Delete One Song",command=del_song)
delete_menu.add_command(label="Delete All Songs",command=del_all)

Time = Label(root,text="",anchor=E,relief=GROOVE,bd=1)
Time.pack(side=BOTTOM,fill=X,ipady=4)

length = ttk.Scale(main_frame,from_=0,to=100,orient=HORIZONTAL,value=0,length=350)
length.grid(row=2,column=0,pady=10)
length['state'] = DISABLED
length.bind('<ButtonRelease-1>',adjust)

volume_frame = LabelFrame(main_frame,text="Volume")
volume_frame.grid(row=0,column=1,padx=20)

volume = ttk.Scale(volume_frame,from_=0,to=1,orient=VERTICAL,value=0,length=180,command=volume_func)
volume.pack()
volume['state']=DISABLED

label = Label(main_frame,text="")
label.grid(row=3,column=0,pady=20)

root.mainloop()