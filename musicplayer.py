import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pygame
import os
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, Tk):
        self.root = Tk
        self.root.title("MUSIC PLAYER")
        self.root.geometry('920x700')
        self.root.configure(background='black')
        self.heading=Label(text="MUSIC",bg="black",fg="white",font=22).place(x=70,y=20)
        self.root.resizable(0,0)
        self.playlist_indices=[]
        
        # Initialize Pygame mixer
        pygame.mixer.init()
        
        self.photo=ImageTk.PhotoImage(file="pic1.jpg")
        Label(self.root, image=self.photo,bg="black").place(x=50,y=50,width=500,height=500)
        
        #buttons
        self.play_button = Button(self.root, text="Play", command=self.play_music, bg="green", fg="white")
        self.play_button.place(x=50, y=570, width=60, height=50)

        self.pause_button = Button(self.root, text="Pause", command=self.pause_music, bg="orange", fg="white")
        self.pause_button.place(x=120, y=570, width=60, height=50)

        self.next_button = Button(self.root, text="Next", command=self.next_music, bg="blue", fg="white")
        self.next_button.place(x=190, y=570, width=60, height=50)

        self.prev_button = Button(self.root, text="Prev", command=self.prev_music, bg="red", fg="white")
        self.prev_button.place(x=260, y=570, width=60, height=50)

        self.load_button = Button(self.root, text="Load Directory", 
                                  command=lambda: self.load(self.playlist), bg="blue", fg="white")
        self.load_button.place(x=450, y=570, width=100, height=50)

        # All the frames
        listbox_frame = LabelFrame(root, text='Playlist', bg='LightBlue')
        listbox_frame.place(x=600, y=200, height=200, width=300)

        self.song_frame = LabelFrame(root, text='Current Song', bg='LightBlue', width=300, height=80)
        self.song_frame.place(x=600, y=100)
        Label(self.song_frame, text='CURRENTLY PLAYING:', bg='LightGreen', 
              font=('Times', 10, 'bold')).place(x=5, y=20)

        #playlist as a ListBox
        self.playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='Gold')
        
        #scroll bar
        scroll_bar = Scrollbar(listbox_frame, orient=VERTICAL)
        scroll_bar.pack(side=RIGHT, fill=BOTH)

        self.playlist.config(yscrollcommand=scroll_bar.set)

        scroll_bar.config(command=self.playlist.yview)

        self.playlist.pack(fill=BOTH, padx=5, pady=5)

        #song label to show currently playing song
        self.song_label=Label(self.song_frame, text='No music selected')
        self.song_label.place(x=5, y=40)


    #function for play button
    def play_music(self):
        if not self.playlist_indices:
            messagebox.showinfo("MESSAGE","PLEASE LOAD DIRECTORY")
            return
        if not self.playlist.curselection():
            messagebox.showinfo("MESSAGE","SELECT A SONG")
            return
        selected_index=self.playlist.curselection()
        
        pygame.mixer.music.load(self.playlist.get(selected_index))
        self.playlist.selection_clear(0,tk.END)
        self.playlist.selection_set(selected_index)
        pygame.mixer.music.play()
        self.song_label.config(text=f'Playing: {self.playlist.get(selected_index)}')
        

    #function for pause button
    def pause_music(self):
        if not self.playlist_indices:
            messagebox.showinfo("MESSAGE","PLEASE LOAD DIRECTORY")
            return
        if not self.playlist.curselection():
            messagebox.showinfo("MESSAGE","SELECT A SONG")
            return
        pygame.mixer.music.pause()
        self.song_label.config(text='Pausing music')
        print("Pausing music")


    #function for next button
    def next_music(self):
        if not self.playlist_indices:
            messagebox.showinfo("MESSAGE","PLEASE LOAD DIRECTORY")
            return
        if not self.playlist.curselection():
            messagebox.showinfo("MESSAGE","SELECT A SONG")
            return
        curindex=self.playlist.curselection()
        next_index=(curindex[0]+1)%self.playlist.size()
        self.playlist.selection_clear(0,tk.END)
        song=self.playlist.get(next_index)
        self.playlist.selection_set(next_index)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.song_label.config(text=f'Playing: {self.playlist.get(next_index)}')
        

    #function for prev button
    def prev_music(self):
        if not self.playlist_indices:
            messagebox.showinfo("MESSAGE","PLEASE LOAD DIRECTORY")
            return
        if not self.playlist.curselection():
            messagebox.showinfo("MESSAGE","SELECT A SONG")
            return
        curindex=self.playlist.curselection()
        prev_index=(curindex[0]-1)%self.playlist.size()
        self.playlist.selection_clear(0,tk.END)
        song=self.playlist.get(prev_index)
        self.playlist.selection_set(prev_index)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.song_label.config(text=f'Playing: {self.playlist.get(prev_index)}')
    

    #function for load button
    def load(self,listbox):
       os.chdir(filedialog.askdirectory(title='Open a songs directory'))
       tracks = os.listdir()
       for track in tracks:
        listbox.insert(END, track)
        self.playlist_indices.append(len(self.playlist_indices))
  

root = Tk()
ob = MusicPlayer(root)
root.mainloop()