
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

<p align="center"><img src="./README_IMAGES/discordmessage.png"></p>

Come si può notare tutti i dati inviati contengono l'id del game, questo perchè potrebbe tornare utile nel caso si voglia, in un implementazione futura, garantire assistenza post game e permettere ad ogni utente di effettuare il rewatch del game.
Tutti i dati sopra riportati verranno mostrati, tramite una GUI, ad ogni utente.



## Architecture

<p align="center"><img src="./README_IMAGES/architecture.png"></p>

- LocalStack is used to emulate the cloud environment and duplicate the AWS services.
- A Python script that uses boto3 to transmit messages on the queues simulates the IoT devices on each player.
- Amazon Simple Queue Service (SQS) is being used to implement the queue.
- Amazon DynamoDB was used to create the database.
- The functions are Serveless functions deployed on AWS Lambda.
- Two IFTT Applets are used to send the message on Discord.
- Dynamodb-admin provides access to the DynamoDB GUI.



# Installation and usage
## Prerequisites 


1. [Docker](https://docs.docker.com/get-docker/)
2. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
4. *(Optional)* nodejs for database visualization.
5. [fastAPI](https://fastapi.tiangolo.com/)
6. [uvicorn](https://www.uvicorn.org/)


## Setting up the environment  

**1. Launch [LocalStack](https://localstack.cloud/)**

`docker run --rm -it -p 4566:4566 -p 4571:4571  localstack/localstack`

if u have some error when you call the Lambda function that ask something like "_mount /var/run/docker.sock:/var/run/docker.sock_" use the following command to run the docker

`docker run --rm -it -p 4566:4566 -p 4571:4571 -v /var/run/docker.sock:/var/run/docker.sock localstack/localstack`


**2. Create a SQS queue for each queue**

`aws sqs create-queue --queue-name Vitality --endpoint-url=http://localhost:4566`

`aws sqs create-queue --queue-name PGNAT --endpoint-url=http://localhost:4566`

`aws sqs create-queue --queue-name Infoqueue --endpoint-url=http://localhost:4566`

`aws sqs create-queue --queue-name Sosqueue --endpoint-url=http://localhost:4566`

- Check that the queues are been correctly created

`aws sqs list-queues --endpoint-url=http://localhost:4566`

**3 Create the DynamoDB tables**

1) Use the python code to create the DynamoDB tables

`python3 createDB.py`

2) Check that the tables are been correctly created

`aws dynamodb list-tables --endpoint-url=http://localhost:4566`

or using the [dynamodb-admin] GUI with the command

`DYNAMO_ENDPOINT=http://0.0.0.0:4566 dynamodb-admin`
and then going to `http://localhost:8001`.





**4. Create the message-triggered Lambda function to store the gps data of each team** 

   1. Create the role 

`aws iam create-role --role-name lambdarole --assume-role-policy-document file://role_policy.json --query 'Role.Arn' --endpoint-url=http://localhost:4566`

   2. Attach the policy

`aws iam put-role-policy --role-name lambdarole --policy-name lambdapolicy --policy-document file://policy.json --endpoint-url=http://localhost:4566`

   3. Create the zip file

`zip SaveGpsData.zip SaveGPSData.py`

   4. Create the Lambda function

`aws lambda create-function --function-name savegpsdata --zip-file fileb://SaveGpsData.zip --handler SaveGPSData.lambda_handler --runtime python3.9 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566`

   5. Create the event source mapping between function and queues

`aws lambda create-event-source-mapping --function-name savegpsdata --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:Vitality --endpoint-url=http://localhost:4566`

`aws lambda create-event-source-mapping --function-name savegpsdata --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:PGNAT --endpoint-url=http://localhost:4566`

**5. Create the message-triggered Lambda function to store info data of each team**
   1. Create the zip file 

`zip sendinfofunc.zip SendInfoFunc.py`

   2. Create the Lambda function

`aws lambda create-function --function-name sendinfofunc --zip-file fileb://sendinfofunc.zip --handler SendInfoFunc.lambda_handler --runtime python3.9 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566`

   3. Create event source mapping between function and queue

`aws lambda create-event-source-mapping --function-name sendinfofunc --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:Infoqueue --endpoint-url=http://localhost:4566`


**Set up the Lambda function triggered by SQS messages that notifies emergency during the game session via Discord and GUI**

We need to create 2 IFTT Applet in order to correctly send data to discord, that because the free to use version of IFTT allow us to pass a maximum of 3 value to discord, but we need 5 values. So to solve this problem we use 2 Applet that work toghether to send message
First of all u need to create a discord server with a text channel

1. Create the first Applet
   1. Go to https://ifttt.com/ and sign-up or log-in if you already have an account.
   2. On the main page, click *Create* to create a new applet.
   3. Click "*If This*", type *"webhooks"* in the search bar, and choose the *Webhooks* service.
   4. Select "*Receive a web request*" and write *"sos_message"* in the "*Event Name*" field. Save the event name since it is required to trigger the event. Click *Create trigger*.
   5. In the applet page click *Then That*, type *"discord"* in the search bar, and select *discord*.
   6. Click *Post a rich message to a channel* and fill the fields as follow:

   - Select the discord server (that you have previously created) where u want to send messages
   - Select the text channel (that you have previously created) where u want to post the message 

         Embed Title= :sos: Player   {{Value1}} request HELP

         Embed Description= Latitude: {{Value2}} ----Longitude:{{Value3}}<br> 
                               https://www.openstreetmap.org/?mlat={{Value2}}&amp;mlon={{Value3}}#map=19/{{Value2}}/{{Value3}}

         Embed Color= ff111

   7. Click *Create action*, *Continue*, and *Finish*.




2. Create the second Applet
   1. On the main page, click *Create* to create a new applet.
   2. Click "*If This*", type *"webhooks"* in the search bar, and choose the *Webhooks* service.
   3. Select "*Receive a web request*" and write *"status_message"* in the "*Event Name*" field. Save the event name since it is required to trigger the event. Click *Create trigger*.
   4. In the applet page click *Then That*, type *"discord"* in the search bar, and select *discord*.
   5. Click *Post a rich message to a channel* and fill the fields as follow:

   - Select the discord server (that you have previously created) where u want to send messages
   - Select the text channel (that you have previously created) where u want to post the message

         Message= STATUS 
                    :heart:Heartbeat {{Value2}}
                    :bubbles:Oxygen {{Value1}}

                     Registered  {{Value3}}
                     ~~                                                          ~~
                     <br>

   6. Click *Create action*, *Continue*, and *Finish*.

3. Modify the variable key within the SendSosMessage.py function with your IFTT applet key (it can be find clicking on the icon of the webhook and clicking on _Documentation_).
4. This lambda function is a function with dependencies, so you need to follow the next steps to create it:
   1. Navigate to the SOSmessage folder 
   2. Install the additional dependencies using pip3 and zip the content of the new folder
      1. `pip3 install --target ./package requests==2.29.0`
      2. `cd package/`
      3. `zip r ../sendsosfunc.zip`
      4. `cd ..`
      5. `zip -g sendsosfunc.zip SendSosMessage.py`
   3. Create the Lambda function

    `aws lambda create-function --function-name sendsosmessage --zip-file fileb://SOSmessage/sendsosfunc.zip --handler SendSosMessage.lambda_handler --runtime python3.9 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566`

   4. Create the event source mapping between function and queue
    
   `aws lambda create-event-source-mapping --function-name sendsosmessage --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:Sosqueue --endpoint-url=http://localhost:4566`
  
If u don't want to do this process manually u can just set up the Applets, change the variable `path` in the file `setup_all.py` with the path of your installation folder and then run it.
It will automatically do for you all the previously commands.

## Use it

**Launch the following command to set up the API**

`uvicorn API:app --reload`

**Launch the GUI on the browser using the file**

`SoftairAssistant.html`

**Launch the script that simulate the game session**

`python3 PlayerSimulation.py`

**Launch Discord and open the server that you have created previously**

At this point you should see the GPS data on the map and all the information about player status on the GUI








  


## Developed by
[Salerno Daniele](https://github.com/DanieleSalerno)


## Future implementations
- [x] Implements the possibility to create account for each player
- [x] Give the possibility to rewatch the game

