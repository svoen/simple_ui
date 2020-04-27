import  multiprocessing as mp
import cv2
import numpy as np
from datetime import datetime
from datetime import timedelta
import os
from AnimatedGIF import *
import serial
import pynmea2
from collections import defaultdict
import numpy as np
import subprocess
import time
import requests
import pytz
import pyaudio
p = pyaudio.PyAudio()
for ii in range(p.get_device_count()):
    print(p.get_device_info_by_index(ii).get('name'))
import wave
import db



IM_WIDTH = 1024 #3264#1024  #Use smaller resolution for
IM_HEIGHT = 768 #2448#768
video = cv2.VideoCapture(0)#manchmal auch 0 evtl try catch einbauen
ret = video.set(3, IM_WIDTH)
ret = video.set(4, IM_HEIGHT)
ret = video.set(6,1196444237)
font = cv2.FONT_HERSHEY_SIMPLEX


port = "/dev/ttyACM0" 

class Processing_window():

    def __init__(self, master, liste, repeat_time, dauer, standort, zeit_einheit):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()

        
        self.var_list = liste
        self.repeat_time = repeat_time.get()
        self.standort = standort.get()
        self.dauer = dauer.get()
        self.zeit_einheit = zeit_einheit.get()
        
        
        self.gestartete_prozesse=[]
        self.gps = defaultdict(list)
        self.mean_gps = {}
        
        
        self.button_frame = tk.Frame(master=self.frame)
        self.button_frame.pack()
        self.text_frame = tk.Frame(master=self.frame)
        self.text_frame.pack()
        self.GIF_frame = tk.Frame(master=self.frame)
        self.GIF_frame.pack()

        
        self.stateButton = tk.Button(master=self.button_frame, text='Start',command=self.sensorselector).pack(fill ='x')
        self.stopButton = tk.Button(master=self.button_frame, text='Back!',command=self.close_app).pack(fill ='x')

        self.scrollbar = tk.Scrollbar(master=self.text_frame)
        self.text_log_feld = tk.Text(master=self.text_frame, width=100, height= 5)
        self.scrollbar.pack(side='right')
        self.text_log_feld.pack(side='left')
        self.scrollbar.config(command=self.text_log_feld.yview)
        self.text_log_feld.config(yscrollcommand=self.scrollbar.set)
        self.text_log_feld.tag_configure('bigred', foreground='red2', font=('Verdana', 19, 'bold'))

        for i in self.var_list:
            count = 0
            if i.get() == 1:
                self.lbl1 = tk.Label(master=self.GIF_frame, text='Please do not disturb bits in progress.').pack(fill='x')
                self.gif = AnimatedGif(self.GIF_frame, 'GIF2.gif',0.1)
                self.gif.pack()
                self.gif.start()
                count+1
                break
        if count == 0:

            self.lbl = tk.Label(master=self.GIF_frame,text= 'No sensor selected, please select a sensor.',foreground='red2', font=('Verdana', 19, 'bold'))

        print(self.zeit_einheit)
        print('2 Seite: hat die ProzessID = ' + str(os.getpid()))
    
    
    def server1090(self):
        bashcommand = 'nohup  /home/pi/Desktop/Tkinter_BA/starter.sh & '
        process = subprocess.Popen(bashcommand.split(),stdout=subprocess.PIPE, shell=False)
   
    
    def GNSS(self):
        #self.text_log_feld.insert('end','GNSS is Running 1 !!!\n')
        print('GNSS: hat die ProzessID ')
        print(os.getpid())
        self.text_log_feld.insert('end','\nStart GNSS-Procces \n')
        i = 1
        serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)
        print("warm up GPS")
        while True:
            try:
                str = serialPort.readline()
                str = str.decode("utf-8")
                if str.find('GGA') > 0:

                    msg = pynmea2.parse(str)
                    print(i, msg)

                    values = str.split(",")

                    gps_time_utc = float(values[1])

                    y = values[2].replace(".", "")
                    x = values[4].replace(".", "")
                    print('test')
                                        
                    altitude = float(values[9])
                    
                    satellites = int(msg.num_sats)

                    deg_lat = float(y[0:2])
                    min_lat = float(y[2:]) / 10E4
                    deg_lon = float(x[1:3])
                    min_lon = float(x[3:]) / 10E4

                    lat = round(deg_lat + min_lat / 60, 5)
                    lon = round(deg_lon + min_lon / 60, 5)

                    if i >= 5:

                        self.gps["lat"].append(lat)
                        self.gps["lon"].append(lon)
                        self.gps["satellites"].append(satellites)
                        self.gps["altitude"].append(altitude)
                        
                        
                    if i == 15:
                        self.mean_gps = {"lat": round(np.mean(self.gps["lat"]),6), "lon": round(np.mean(self.gps["lon"]),6), "altitude": round(np.mean(self.gps["altitude"]),1),
                               "satellites": round(np.mean(self.gps["satellites"]),1)}
                        print(self.gps)

                        sql = '''INSERT INTO public.gps (lat, lon, altitude, satellite) VALUES (%s, %s, %s, %s);'''

                        vals = [self.mean_gps['lat'],
                                self.mean_gps['lon'],
                                self.mean_gps['altitude'],
                                self.mean_gps['satellites']]
                        db.execute((sql, vals))
                        print('in db geschreieben')
                               
                        self.text_log_feld.insert('end','Average measurements saved to database! \n')
                        print(os.getpid())                       
                        return True
                    
                    i += 1
            except Exception as e:
                print(e)
                print("no gpsinfo")
                self.text_log_feld.insert('end','No Gps data could be received! \n')
                return False
      

    def SDR(self):
        print('SDR: hat die ProzessID = ' + str(os.getpid()))        
        url = 'http://0.0.0.0:8080/data.json'
        response = requests.get(url)
        data = response.json()
        server_timezone = pytz.timezone("Europe/Amsterdam")
        server_time = datetime.now(server_timezone)
        
        if self.dauer == '' or self.zeit_einheit == '':
            self.text_log_feld.insert('end','\nNo measurement duration and no timeunit specified!\n\n','bigred')
            
        if self.dauer != '' and self.zeit_einheit != '':
            if self.zeit_einheit == 'sec': stop_time = datetime.now()+timedelta(seconds=int(self.dauer))#Laufzeitvariable Sekunden
            if self.zeit_einheit == 'min': stop_time = datetime.now()+timedelta(minutes=int(self.dauer))#Laufzeitvariable Minuten
            
            while datetime.now() <= stop_time:
                
                if len(data) >= 0:
                    for flight in data:
                        info = {"hex": flight["hex"], "squawk": flight["squawk"], "flight": flight["flight"], "speed": flight["speed"],
                                "lat": flight["lat"], "lon": flight["lon"], "track": flight["track"], "validposition": flight["validposition"], "validtrack": flight["validtrack"],
                                "messages": flight["messages"], "seen": flight["seen"],
                                "altitude": flight['altitude'], "vert_rate": flight["vert_rate"]
                                }#"timestamp": server_time['timestamp']
                        print(info)

                        sql = '''INSERT INTO public.flightdata (hex, squawk, flight, speed, lat, lon, track, validposition, validtrack, messages, seen, altitude, vert_rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

                        vals = [info['hex'],
                                info['squawk'],
                                info['flight'],
                                info['speed'],
                                info['lat'],
                                info['lon'],
                                info['track'],
                                info['validposition'],
                                info['validtrack'],
                                info['messages'],
                                info['seen'],
                                info['altitude'],
                                info['vert_rate']
                                ]#info['timestamp']
                        db.execute((sql, vals))
                        print('in db geschreieben')                        
                                                        
                if len(data) == 0:
                    print('No data receved')               
        print('SDR Done')
    
    def Kamera_P(self):
        print('Kamera: hat die ProzessID = ' + str(os.getpid()))
        if self.dauer == '' or self.repeat_time == ''or self.zeit_einheit == '':
            self.text_log_feld.insert('end','\nNo measurement duration,interval and or\nno timeunit specified!\n\n','bigred')
            return
        if self.dauer != '' and self.repeat_time != ''and self.zeit_einheit != '':
            if self.zeit_einheit == 'sec': stop_time = datetime.now()+timedelta(seconds=int(self.dauer))#Laufzeitvariable Sekunden
            if self.zeit_einheit == 'min': stop_time = datetime.now()+timedelta(minutes=int(self.dauer))#Laufzeitvariable Minuten
            if self.zeit_einheit == 'min': save_intervall = datetime.now()+timedelta(minutes=int(self.repeat_time))
            if self.zeit_einheit == 'sec': save_intervall = datetime.now()+timedelta(seconds=int(self.repeat_time))
            
            self.text_log_feld.insert('end','Camera measurement begins!\n')
            count = 1
            while datetime.now() <= stop_time:
 
                freq = cv2.getTickFrequency()
                fps = video.get(5)
                ret, frame = video.read()
                cv2.putText(frame,"FPS: {0:.2f} {0:.2f}".format(fps, freq),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
                #cv2.imshow("frame", frame)

                
                if datetime.now().strftime("%H:%M:%S") == save_intervall.strftime("%H:%M:%S"):                   
                    print('Save')
                    cv2.imwrite('/home/pi/Desktop/Tkinter_BA/records/photo/photo'+str(count)+'.jpg', frame)
                    count = count+1
                    print(count)
                    if self.zeit_einheit == 'min': save_intervall = datetime.now()+timedelta(minutes=int(self.repeat_time))
                    if self.zeit_einheit == 'sec': save_intervall = datetime.now()+timedelta(seconds=int(self.repeat_time))

                key = cv2.waitKey(1)
                if key == 27:
                    break
            video.release()
            cv2.destroyAllWindows()
        self.text_log_feld.insert('end','Camera measurement is finished!\n')
    
    def Kamera_V(self):
        print('Kamera: hat die ProzessID = ' + str(os.getpid()))
        if self.dauer == '' or self.repeat_time == ''or self.zeit_einheit == '':
            self.text_log_feld.insert('end','\nNo measurement duration,interval and or\nno timeunit specified!\n\n','bigred')
            return
        if self.dauer != '' and self.repeat_time != ''and self.zeit_einheit != '':
            if self.zeit_einheit == 'sec': stop_time = datetime.now()+timedelta(seconds=int(self.dauer))#Laufzeitvariable Sekunden
            if self.zeit_einheit == 'min': stop_time = datetime.now()+timedelta(minutes=int(self.dauer))#Laufzeitvariable Minuten
            if self.zeit_einheit == 'min': save_intervall = datetime.now()+timedelta(minutes=int(self.repeat_time))
            if self.zeit_einheit == 'sec': save_intervall = datetime.now()+timedelta(seconds=int(self.repeat_time))
            self.text_log_feld.insert('end','Camera measurement begins!\n')
            out = cv2.VideoWriter('/home/pi/Desktop/Tkinter_BA/records/video/record.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (IM_WIDTH, IM_HEIGHT))

            while datetime.now() <= stop_time:  
                freq = cv2.getTickFrequency()
                fps = video.get(5)
                ret, frame = video.read()
                cv2.putText(frame,"FPS: {0:.2f} {0:.2f}".format(fps, freq),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
                out.write(frame)
                cv2.imshow("frame", frame)
              
                if datetime.now().strftime("%H:%M:%S") == save_intervall.strftime("%H:%M:%S"):
                    print('Save')
                    if self.zeit_einheit == 'min': save_intervall = datetime.now()+timedelta(minutes=int(self.repeat_time))
                    if self.zeit_einheit == 'sec': save_intervall = datetime.now()+timedelta(seconds=int(self.repeat_time))
                 
                key = cv2.waitKey(1)
                if key == 27:
                    break
            video.release()
            out.release()
            cv2.destroyAllWindows()
        self.text_log_feld.insert('end','Camera measurement is finished!\n')
    
    
    
    def Mikrofon(self):
        print('Mikrofon: hat die ProzessID = '+str(os.getpid()))
        if self.dauer == '' or self.zeit_einheit == '':
            self.text_log_feld.insert('end','No recording time or timeunit set!\n','bigred')
            return
        
        form_1 = pyaudio.paInt16 # 16-bit resolution
        chans = 1 # 1 channel
        samp_rate = 44100 # 44.1kHz sampling rate
        chunk = 4096 # 2^12 samples for buffer
        record_secs = int(self.dauer) # seconds to record
        
        dev_index = 2 # device index found by p.get_device_info_by_index(ii)
        wav_output_filename = '/home/pi/Desktop/Tkinter_BA/records/sound/test1.wav' # name of .wav file
        audio = pyaudio.PyAudio() # create pyaudio instantiatio
        # create pyaudio stream
        stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                            input_device_index = dev_index,input = True, \
                            frames_per_buffer=chunk)
        print("recording")
        frames = []
        # loop through stream and append audio chunks to frame array
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            data = stream.read(chunk)
            frames.append(data)
        print("finished recording")
        # stop the stream, close it, and terminate the pyaudio instantiation
        stream.stop_stream()
        stream.close()
        audio.terminate()
        # save the audio frames as .wav file
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()


    def sensorselector(self):
   
        for i in self.var_list:
            count = 0
            if i.get() == 1:
                self.text_log_feld.insert('end','measurement begins if measuring time specified!\n')
                count = count+1
                print(count)
                break
        if count == 0:
            self.text_log_feld.insert('end','No sensor selected, please select a sensor!\n', 'bigred')


        if self.var_list[0].get() == 1:
            self.p1 = mp.Process(target=self.GNSS())
            self.gestartete_prozesse.append('GPS')
            self.p1.start()
            
        if self.var_list[1].get() == 1:
            ps = mp.Process(target=self.server1090())
            ps.start()
            time.sleep(2)        
            self.p2 = mp.Process(target=self.SDR())
            self.gestartete_prozesse.append('SDR')
            self.p2.start()
        
        if self.var_list[2].get() == 1:
            self.p3 = mp.Process(target=self.Kamera_P())
            self.gestartete_prozesse.append('Kamera_P')
            self.p3.start()
        
        if self.var_list[3].get() == 1:
            self.p4 = mp.Process(target=self.Mikrofon())
            self.gestartete_prozesse.append('Mikrofon')
            self.p4.start()
        
        if self.var_list[4].get() == 1:
            self.p5 = mp.Process(target=self.Kamera_V())
            self.gestartete_prozesse.append('Kamera_V')
            self.p5.start()
            
            
    def close_app(self):
       
        for i in self.gestartete_prozesse:
            if i == 'GPS':
                self.p1.terminate()
            if i == 'SDR':   
                bashcomand = 'sudo killall dump1090 '
                process = subprocess.Popen(bashcomand.split(),stdout=subprocess.PIPE, shell=False)
                time.sleep(2)
                self.p2.terminate()
            if i == 'Kamera_P':
                self.p3.terminate()
            if i == 'Mikrofon':
                self.p4.terminate()
            if i == 'Kamera_V':
                self.p5.terminate()
        self.text_log_feld.delete('0.0', 'end')
        self.master.destroy()
