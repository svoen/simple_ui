import requests, json
import tkinter as tk
from tkinter import ttk
from GUI_Colector_Secondpage import Processing_window
import subprocess
import time

class Start_Window:

    def __init__(self,master):
        
        self.tkFenster = master
        self.tkFenster.title('Geodatencolektor')
        self.tkFenster.geometry('440x350') #350X350

       
        self.int_var1 = tk.IntVar()
        self.int_var2 = tk.IntVar()
        self.int_var3 = tk.IntVar()
        self.int_var4 = tk.IntVar()
        self.int_var5 = tk.IntVar()
        self.int_var6 = tk.IntVar()
        self.int_var7_video = tk.IntVar()
        self.interval_text = tk.StringVar()
        self.dauer_text = tk.StringVar()
        self.standort_text = tk.StringVar()
        self.zeit_einheit = tk.StringVar()

       
        self.labelFrame = tk.Frame(master=master)
        self.labelFrame.grid(row=0, column=0, padx='5', pady='5')
        self.inputFrame = tk.Frame(master=master)
        self.inputFrame.grid(row=0, column=1, padx='5', pady='5')
        self.checkbuttonFrame = tk.Frame(master=master)
        self.checkbuttonFrame.grid(row=1, column=0, padx='5', pady='5')
        self.buttonFrame = tk.Frame(master=master)
        self.buttonFrame.grid(row=3, column=0, padx='5', pady='5')
        

        
        self.standort_label = tk.Label(master=self.labelFrame, text = 'location')
        self.standort_label.pack()
        self.interval_label = tk.Label(master=self.labelFrame, text='repetition rate!')
        self.interval_label.pack()
        self.aufnahme_dauer = tk.Label(master = self.labelFrame, text = 'recording duration')
        self.aufnahme_dauer.pack()
        self.time_unit = tk.Label(master = self.labelFrame, text = 'time unit')
        self.time_unit.pack()

        
        self.standort = tk.Entry(master=self.inputFrame, textvariable=self.standort_text)
        self.standort.pack()
        self.interval = tk.Entry(master=self.inputFrame,  textvariable=self.interval_text)
        self.interval.pack()
        self.dauer = tk.Entry(master=self.inputFrame, textvariable=self.dauer_text)
        self.dauer.pack()
        
        
        self.sec_Radiobutton = tk.Radiobutton(master=self.inputFrame, anchor='w',text='Sec', value='sec', variable=self.zeit_einheit)
        self.sec_Radiobutton.pack(side='left')
        self.min_Radiobutton = tk.Radiobutton(master=self.inputFrame, anchor='w',text='Min', value='min', variable=self.zeit_einheit)
        self.min_Radiobutton.pack(side='left')

        
        self.checkbutton1 = tk.Checkbutton(master=self.checkbuttonFrame, text='GNSS', indicatoron=0, width=20, padx=20,  variable=self.int_var1).pack()
        self.checkbutton2 = tk.Checkbutton(master=self.checkbuttonFrame, text='SDR-Dongel', indicatoron=0, width=20, padx=20, variable=self.int_var2).pack()
        self.checkbutton3 = tk.Checkbutton(master=self.checkbuttonFrame, text='USB-Kamera (Photo)', indicatoron=0, width=20, padx=20, variable=self.int_var3).pack()
        self.checkbutton4 = tk.Checkbutton(master=self.checkbuttonFrame, text='USB-Kamera (Video)',indicatoron=0,width=20, padx=20, variable=self.int_var7_video).pack()
        self.checkbutton5 = tk.Checkbutton(master=self.checkbuttonFrame, text='USB-Mikrofon', indicatoron=0, width=20, padx=20, variable=self.int_var4).pack()
        #self.checkbutton6 = tk.Checkbutton(master=self.checkbuttonFrame, text='Wetter-AP', indicatoron=0, width=20, padx=20, variable=self.int_var5).pack()
        #self.checkbutton7 = tk.Checkbutton(master=self.checkbuttonFrame, text='Flightradar-AP', indicatoron=0, width=20, padx=20, variable=self.int_var6).pack()

        
        #self.stateButton = tk.Button(master=self.buttonFrame, text='Check Checkbox state!', width=25, command= self.check_variable).pack()
        self.startButton = tk.Button(master=self.buttonFrame, text='Start colector!', width=25, command=self.open_collecting_window).pack()
        self.stopButton = tk.Button(master=self.buttonFrame,text='Stop application', width=25,  command=self.close_app).pack()


    def open_collecting_window(self):
       
        self.newWindow = tk.Toplevel(self.tkFenster)
        self.newWindow.geometry('500x500')
        int_list = [self.int_var1, self.int_var2, self.int_var3 ,self.int_var4 , self.int_var7_video]
        repeat_time = self.interval_text
        dauer = self.dauer_text
        standort = self.standort_text
        zeit_einheit = self.zeit_einheit
       
        self.app = Processing_window(self.newWindow, int_list, repeat_time, dauer, standort, zeit_einheit)

    def close_app(self):
        bashcomand = 'sudo killall postgresql'
        process = subprocess.Popen(bashcomand.split(),stdout=subprocess.PIPE, shell=False)
        time.sleep(2)
        self.tkFenster.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = Start_Window(root)
    root.mainloop()
