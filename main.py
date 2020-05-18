import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')

statusbar = ttk.Label(root, text='Welcome to Music', relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)
# Create Menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create submenus
subMenu = Menu(menubar, tearoff=0)

playlist = []


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


def about_us():
    tkinter.messagebox.showinfo('Music Player', 'Created by Jeba Sam')


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


def on_closing():
    stop_music()
    root.destroy()


def start_count(t):
    global paused
    # Returns False when press stop button
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            current_time_label['text'] = 'Current Time ' + ' ' + timeformat
            time.sleep(1)
            current_time += 1


def show_details(play_song):
    file_data = os.path.splitext(play_song)
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    length_label['text'] = 'Total Length ' + ' ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = 'Resumed Music'
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
            statusbar['text'] = 'Playing Music' + ' ' + os.path.basename(play_it)
            show_details(play_it)

        except:
            tkinter.messagebox.showerror('File Not Found', 'Music Is not Found .Check for Music')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'Music Stopped'


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = 'Music Paused'


def rewind_music():
    play_music()
    statusbar['text'] = 'Music Rewinded'


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # mixer  takes volume in 0 or 1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # Mute
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


menubar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='About Developer', command=about_us)

mixer.init()

root.title("Music Player")
root.iconbitmap(r'Images/music_player.ico')

left_frame = ttk.Frame(root)
left_frame.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(left_frame)
playlistbox.pack()

addBtn = ttk.Button(left_frame, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)

delBtn = ttk.Button(left_frame, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

right_frame = ttk.Frame(root)
right_frame.pack(pady=30)

top_frame = ttk.Frame(right_frame)
top_frame.pack()

length_label = ttk.Label(top_frame, text='Total Length : --:--')
length_label.pack(pady=10)

current_time_label = ttk.Label(top_frame, text='Current Time : --:--', relief=GROOVE)
current_time_label.pack()

middle_frame = ttk.Frame(right_frame)
middle_frame.pack(pady=30, padx=30)

playPhoto = PhotoImage(file='Images/play.png')
playBtn = ttk.Button(middle_frame, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='Images/stop.png')
stopBtn = ttk.Button(middle_frame, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='Images/pause.png')
pauseBtn = ttk.Button(middle_frame, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

bottom_frame = ttk.Frame(right_frame)
bottom_frame.pack(pady=10)

rewindPhoto = PhotoImage(file='Images/rewind.png')
rewindBtn = ttk.Button(bottom_frame, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='Images/mute.png')
volumePhoto = PhotoImage(file='Images/volume.png')
volumeBtn = ttk.Button(bottom_frame, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)

root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()
