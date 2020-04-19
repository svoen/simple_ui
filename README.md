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

