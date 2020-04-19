# simple_ui
User interface for a raspberry pi based geodata-collector. The user interfache provides a simple access to the central functions of the geodata-collector: 
* The sensor selection of the corresponding geodata
  * GPS
  * SoftwareDefinedRadio with Dump1090 Software for ADS-B Aircraft Data retrievment
  * camera for capturing videos or stills
  * microphone for audio recordings
  
* sensors necessarily needed:
  * USB GPS module
  * USB campera
  * USB microphone
  * USB SDR-Reciever
  
  
The collected data will be stored in a local postgreSQL database. A manual configuration of the database and tables is needed in beforehand. Furthermore the creation of a storage folder for the video and audio is mendatory to fit the scripts.

Also there are 3 .stl files for a 3d printed collector case which serve as a showcase and hence makes the collector a portable unit for the field.



![front](https://i.ibb.co/VVc3rXz/a92b7a89-cdda-47a0-9801-896eecc14857.jpg)

![detail front](https://i.ibb.co/zXfBdHd/f7f22fae-42e1-4aa0-9b28-d4740aa16729.jpg)

![inside](https://i.ibb.co/tYTPmpr/f8426ceb-ca40-4709-81db-7140f7d68690.jpg)

![front sensors](https://i.ibb.co/FJjNs9k/a8a53236-c672-48e9-be44-088e7793a8ce.jpg)






