
<p align="center"><img src="./README_IMAGES/logo.png" height="250"></p>

# SoftairAssistant
## Overview
SoftairAssistant è un progetto che mira a sviluppare un dispositivo in grado di assistere i iocatori di softair durante le sessioni di gioco. Si pone l'obiettivo di fornire assistenza real time durante le sessioni di gioco fornendo informazioni relative alla posizione GPS dei membri del team, alla quantità di munizioni rimaste per ogni player e la precisione media del team. Inoltre, in caso di emergenza, fornisce le informazioni necessarie per intervenire nel modo più veloce possibile. 

Il progetto è basato su un IoT Cloud Architecture dove diversi sensori IoT collezionano dati e li inviano sul cloud dove verranno processati attraverso computazione serverless e salvati in un NoSQL database per essere facilmente accessibili
I sensori sono piazzati su ogni giocatore e ne misurano la posizione GPS,il battito cardiaco,il livello di ossigeno nel sangue. Inoltre ogni player è equipaggiato con un giubbotto antiproiettile dotato di lettore RFID in grado di riscontrare da chi è stato colpito il giocatore leggendo l'RFID integrato nei proiettili.
Esiste una coda per ogni team su di cui ogni sensore invierà dati contenenti le seguenti informazioni
- The ID of the player;
- time in format yyyy-mm-dd hh:mm:ss;
- latitude;
- longitude;
- The ID of the game;

Each time a message appear on these queue, an event triggered Servereless function save the data on the database

Inoltre è presente una coda relativa alle informazioni di ogni game su di cui verranno inviate i seguenti dati:
- the ID of the player hitted;
- time in format yyyy-mm-dd hh:mm:ss;
- the ID of the player who made the shot;
- the number of remaining lives of the hitted player

Tutti questi dati verranno salvati mediante un event triggered Serverless function sul database.

Infine è presente un'ultima coda relativa alle emergenze su di cui verranno inviate le seguenti informazioni:
- The ID of the player that call the SOS;
- time in format yyy-mm-dd hh:mm:ss;
- latitude;
- longitude;
- The ID of the game;
- oxygen level;
- heartbeat;
- the status of emergency;

Tutti i dati verranno poi memorizzati in un database utilizzando un event triggered Serverless function
Nel momento in cui avviene un'emergenza la partita verrà messa in pausa e verrà inviato un messaggio sul canale discord dell'admin contenente tutte le informazioni sopra elencate. Nel momento in cui l'emergenza sarà risolta l'admin potrà far riprendere la sessione di gioco.

Come si può notare tutti i dati inviati contengono l'id del game, questo perchè potrebbe tornare utile nel caso si voglia, in un implementazione futura, garantire assistenza post game e permettere ad ogni utente di effettuare il rewatch del game.
Tutti i dati sopra riportati verranno mostrati, tramite una GUI, ad ogni utente.

## Requisiti 
Prima di iniziare bisogna installare:

- python 3.9
- docker 
- localstack
- fastAPI
- uvicorn


## how to do 
There are two ways to set up all the necessary element:

- write every single operation in the cmd 
- run the setup_all file available in the repository and change the content of the Variable PATH with the installation folder of the project

1. Run localstack on docker 
   1. docker run --rm -it -p 4566:4566 -p 4571:4571  localstack/localstack
2. if u have some error when u call the Lambda function that ask something like "mount /var/run/docker.sock:/var/run/docker.sock" use the followinf command to run the docker
   2. docker run --rm -it -p 4566:4566 -p 4571:4571 -v /var/run/docker.sock:/var/run/docker.sock localstack/localstack

From this point u need to chose if you want to use the setup_file or if you don't want
3. create all the queue

   1. `aws sqs create-queue --queue-name Vitality --endpoint-url=http://localhost:4566`
   2. `aws sqs create-queue --queue-name PGNAT --endpoint-url=http://localhost:4566`
   3. `aws sqs create-queue --queue-name Infoqueue --endpoint-url=http://localhost:4566`
   4. `aws sqs create-queue --queue-name Sosqueue --endpoint-url=http://localhost:4566`

4. Then u need to create and add the role and add the policy
   1. `aws iam create-role --role-name lambdarole --assume-role-policy-document file://role_policy.json --query 'Role.Arn' --endpoint-url=http://localhost:4566`
   2. `aws iam put-role-policy --role-name lambdarole --policy-name lambdapolicy --policy-document file://policy.json --endpoint-url=http://localhost:4566`




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
