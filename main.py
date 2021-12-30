import os
from tkinter import *
from mutagen.mp3 import MP3
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
import time
import threading
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()         #Returns a list  of all themes that can be set
root.set_theme("itft1")  #Sets am available theme


statusbar = ttk.Label(root, text="Welcome to Nirvana Player", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)



# Create the menu bar
menubar = Menu(root)
root.config(menu=menubar)

# Create submenu

subMenu = Menu(menubar, tearoff=0)

playlist = []

#Plylist it contain the full path + filename
#playlistbox - contains just the filename
#Fullpath - filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Nirvana Player ',
                                'This is the Music Player System built using python Tkinter by Rahul ,Sushma ,Divya ')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initalizating

# root.geometry('300x300')
root.title("Nirvana Player  ")
root.iconbitmap(r'Images/Nirvana Player.ico')

#Root Window - StatusBar, LeftFrame, RightFrame
#LeftFrame - The listbox(playlist)
#RightFrame - TopFrame,MiddleFrame and the BottomFrame

leftframe = Frame(root)
leftframe.pack(side = LEFT,padx = 30,pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add",command=browse_file)
addBtn.pack(side = LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)   # This is use to delete the playlist so that size of the array do not become to much



delBtn = ttk.Button(leftframe, text="- Delete",command = del_song)
delBtn.pack(side = LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)


topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length - --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text='Current Time - --:--', relief=GROOVE)
currenttimelabel.pack()


def show_details(play_song):  # for wave not mp3

    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':  # checks whether it is mp3 file or not
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    minus = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(minus, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # continue - Ignores all the statements below it.We check if music is paused or not
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            minus = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(minus, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]

            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found ',
                                         'RSD Player could not find the file . Please check it again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set volume of mixer takes value only from 0 to 1 .Example - 0,0.1,0.55,0.54,0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)  # Another hidden window
middleframe.pack(pady=10, padx=30)

playPhoto = PhotoImage(file='Images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10, pady=20)

stopPhoto = PhotoImage(file='Images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10, pady=20)

pausePhoto = PhotoImage(file='Images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10, pady=20)

# Buttom Frame for volume ,rewind,mute etc.

bottomframe = Frame(rightframe)  # Another hidden window
bottomframe.pack(pady=10)

rewindPhoto = PhotoImage(file='Images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='Images/mute.png')
volumePhoto = PhotoImage(file='Images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)  # Implement the default value of the scale when the music player start
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
