
<p align="center"><img src="./README_IMAGES/logo.png" height="250"></p>

# SoftairAssistant
## Overview
SoftairAssistant è un progetto che mira a sviluppare un dispositivo in grado di assistere i iocatori di softair durante le sessioni di gioco. Si pone due obiettivi:

+ **Assistenza in real time**: Permette di visualizzare la posizione e lo status di ogni componente del team
+ **Assistenza post game**: Permette di riguardare le partite già giocate in modo da poterle analizzare 

Il progetto è basato su un IoT Cloud Architecture dove diversi sensori IoT collezionano dati e li inviano sul cloud dove verranno processati attraverso computazione serverless e salvati in un NoSQL database per essere facilmente accessibili
I sensori sono piazzati su ogni giocatore e ne misurano la posizione GPS,il battito cardiaco,il livello di ossigeno nel sangue. Inoltre ogni player è equipaggiato con un giubbotto antiproiettile dotato di lettore RFID in grado di riscontrare da chi è stato colpito il giocatore leggendo l'RFID integrato nei proiettili.
Esiste una coda per ogni team e ogni sensore invierà dati contenenti le seguenti informazioni
- The ID of the player;
- time in format yyyy-mm-dd hh:mm:ss;
- latitude;
- longitude;
- Oxygen Level;
- Heartbet ratio;
- 
- 
  Each time a message appear on a queue, an event triggered Servereless function save the data on the database
- name of the city;
- time of the computation in format yyyy-mm-dd hh:mm:ss;
- average temperature;
- ID of the devices that sent the data.

## Management of MIDI Messages
The module for the management of midi messages has been realized entirely in C# language using the library *Sanford.Multimedia.Midi*, which allows to perform all the necessary operations in a MIDI environment, such as creating, receiving and sending MIDI messages. In addition, the *LoopMidi* software was used to create the virtual MIDI ports required for the system to function. Various tests were performed using some of the most popular Digital Audio Workstations and they all proved successful.

## Graphic interface
the graphic interface was created entirely using the 3D graphics engine. There are three screens:


### MainScene
The MainScene is the home page of the system and allows access to the different screens of the system and to manage the configurations allowing to change, export or import a configuration.
![alt text](https://github.com/musimathicslab/marco_smiles/blob/SalernoDaniele-2022/MainScene.jpeg?raw=true)

### TrainScene
The TrainScene allows the user to train the system and thus associate a hand configuration to a certain note, or to the pause. Then, once the recording phase of the various configurations is over, the user can launch the machine learning script and wait for the completion of the training phase.
![alt text](https://github.com/musimathicslab/marco_smiles/blob/SalernoDaniele-2022/trainingScene.jpeg?raw=true)
### PlayScene
The PlayScene allows the user to play the musical instrument. The user in this scene can enable or disable the MIDI functionality. A Sinth allows the user to modify the sound of the instrument through the use of Knob.
![alt text](https://github.com/musimathicslab/marco_smiles/blob/SalernoDaniele-2022/PlayScene.jpeg?raw=true)

## Developed by
[Salerno Daniele](https://github.com/DanieleSalerno)

### Under Supervision of:
[De Prisco Roberto](https://github.com/robdep)

[Zaccagnino Rocco](https://github.com/rzaccagnino)

## Future implementations
- [x] Playing multiple notes at once
- [x] Evolving the system as a tool that takes advantage of virtual reality
- [x] Leveraging cloud services to perform the training phase
- [x] Use more sensors and more features
