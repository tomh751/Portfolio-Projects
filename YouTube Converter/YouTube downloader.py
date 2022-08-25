#!/usr/bin/env python
# coding: utf-8

# In[10]:


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import urllib.request, io
from PIL import ImageTk, Image
from pytube import YouTube
import os


# In[3]:


# A function to return the full path of the files.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_songs(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    downloaded_file = video.download()
    base, ext = os.path.splitext(downloaded_file)
    new_file = base + '.mp3'
    os.rename(downloaded_file, new_file)
    print("Done")


# In[17]:


win = tk.Tk()
win.title('YouTube Downloader')

win_width = 400
win_height = 300

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

x_cord = (screen_width/2) - (win_width/2)
y_cord = (screen_height/2) - (win_height/2)
win.geometry(f'{win_width}x{win_height}+{int(x_cord)}+{int(y_cord)}')

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', anchor='center', font=('calibri', 12), focuscolor='#CD322D')
style.map('TButton', foreground=[('!disabled', 'red'), ('active', 'red')],
          background=[('!disabled', 'white'), ('active', 'white')],
          bordercolor=[('!disabled', '#CD322D'), ('active', '#CD322D')],
          borderwidth=[('!disabled', 0), ('active', 0)])


canvas = tk.Canvas(win, width=400, height=300)
canvas.pack(fill='both', expand=True)
picture = tk.PhotoImage(file=resource_path('youtube logo.png'), master=win)
canvas.create_image(0, 0, image=picture, anchor='nw')
canvas.create_text(80,235,fill='white',font='calibri 13 bold',
                        text='URL:')

url_entry = tk.Entry(win)
url_entry.config(highlightthickness=2, highlightbackground='#CD322D', highlightcolor='#CD322D')
url_entry.place(relx=0.25, rely=0.75, relwidth=0.5)

def get_songs():
    yt = YouTube(url_entry.get())
    video = yt.streams.filter(only_audio=True).first()
    downloaded_file = video.download(output_path=r'C:\Users\User\Downloads')
    base, ext = os.path.splitext(downloaded_file)
    new_file = base + '.mp3'
    os.rename(downloaded_file, new_file)
    msg = tk.messagebox.showinfo('Song Download', f'{video.title} Was download Succsefully!')
    print("Done")

btn = ttk.Button(master=win, text='Download', cursor='hand2', command=get_songs)
btn.place(relx=0.392, rely=0.85, relwidth=0.2, relheight=0.1)



win.resizable(False, False)
win.iconbitmap(resource_path('youtube_logo_for_icon.ico'))
win.mainloop()


# In[ ]:




