import yt_dlp as youtube_dl
import numpy as np
import pydub
import audio2numpy as a2n
from tkinter import filedialog
import os

class UI:
    def __init__(self,urltext):
        self.urltext = urltext 
        self.url = None 
        self.originalfilename = None 
        self.songfilepath = None
        #options for yt_dlp
        self.options = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'keepvideo':False,
            'outtmpl': 'temp.mp3'
        }

    def ask_directory(self):
        path = filedialog.askdirectory()
        return path

    def mp3_to_numpy(self):
        sound_array, sr = a2n.audio_from_file(self.originalfilename)
        return sr, sound_array

    def numpy_to_mp3(self,sound_array,sr):
        channels = 1
        if (sound_array.ndim == 2 and sound_array.shape[1] == 2):
            channels = 2
        sound = np.int16(sound_array*2**15)
        mp3 = pydub.AudioSegment(sound.tobytes(),frame_rate=sr,sample_width=2,channels=channels)
        mp3.export(self.songfilepath,format='mp3',bitrate='320k')

    def nightcorify(self,sound_array):
        # keeping indices with 1.5 step will multiply the frequency by 1.5 
        # and divide the duration by 1.5
        indices = np.around(np.arange(0,len(sound_array),1.5),decimals=0)
        indices = indices[indices < len(sound_array)].astype(int)
        # new sound array 
        sound_array = sound_array[indices.astype(int)] 
        return sound_array 

    def go(self):
        if self.originalfilename == None or self.songfilepath == None:
            return
        sr,sound_array = self.mp3_to_numpy()
        #print(sound_array)
        sound_array = self.nightcorify(sound_array)
        self.numpy_to_mp3(sound_array,sr)
    
    def get_url(self):
        self.url = self.urltext.get('1.0','end')

    #download the mp3 file from a youtube link
    def download_file(self):
        self.get_url()
        path = self.ask_directory()
        try:
            video_info = youtube_dl.YoutubeDL().extract_info(
                url = self.url,download=False
            )
            video_title = video_info['title']
            self.originalfilename = video_title + '.mp3'
            self.options['outtmpl'] = self.originalfilename
            with youtube_dl.YoutubeDL(self.options) as ydl:
                ydl.download([video_info['webpage_url']])
        except youtube_dl.utils.DownloadError: 
            print('invalid URL!')
        self.songfilepath = (path + '\\' + 
            self.originalfilename + ' nightcore.mp3')
        self.go()
        os.remove(self.originalfilename)