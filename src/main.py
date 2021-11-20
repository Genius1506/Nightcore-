import tkinter as tk
from UI import UI

# Initalize tkinter 
root = tk.Tk() 
root.title('Nightcore+')
root.geometry('600x400')
root.tk.call('wm','iconphoto', root._w, tk.PhotoImage(file='imgs/icon.png'))
root.resizable(False,False)
root['bg'] = '#2C303A'

text = tk.Label(root, height=2, width=70, bg='#2C303A', fg='#FFFFFF', bd=0, text='Youtube URL:')
text.config(font=('Courier',20))
text.pack(pady=20)

youtubelink = tk.Text(root, height=2, width=70)
youtubelink.pack(pady=30)

ui = UI(youtubelink) # Object with UI functions

# Upload File Button
download_img = tk.PhotoImage(file='imgs/download-button.png')
download_button = tk.Button(root,image=download_img,command=ui.download_file,border='0')
download_button.pack(pady=40)

root.mainloop() 