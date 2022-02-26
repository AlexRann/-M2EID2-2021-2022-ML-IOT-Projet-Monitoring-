# [ M2EID2, 2021-2022, ML-IOT ] Projet Monitoring [PROTOTYPE]


## Projet académique d'un système de surveillance d'examen à distance "automatisé"


<br><br>


Le projet présente deux parties :
- une partie application mobile
- une partie logiciel PC


![ExamMonitoringSystem_minimal_configuration](https://user-images.githubusercontent.com/64136133/155857299-24683dbd-fdde-454b-8fbf-b6fb98de913c.png)


<br><br>


## Partie application mobile
L'application mobile a pour but l'envoi de message au serveur, dont ce dernier va traiter les messages reçus.<br>
Les messages envoyés par l'application mobile sont principalement les suivantes : 
- la détection de mouvement effectuée par l'accéléromètre 
- l'envoi des photos capturés par sa caméra.


<br><br>


## Partie logiciel PC 
Le logiciel PC a pour de surveiller le candidat à l'examen.<br>
Pour cela, il va analyser la caméra ainsi que l'audio capté par l'ordinateur, ce qui va permettre de :
- la reconnaissance du candidat / nombre de personnes dans la pièce
- la reconnaissance d'objets
- la détection de mouvements (par soustraction d'images)


<br><br>


## Prérequis
- Un ordinateur sous Windows, avec caméra et micro
- Un smartphone doté d'une caméra et d'un accéléromètre


## Comment lancer le projet
(0) Installez les librairies/commandes suivantes :<br>
pip install –upgrade pip<br>
pip install Cmake<br>
conda install -c conda-forge dlib<br>
pip install face_recognition<br>
pip install SpeechRecognition<br>
pip install pipwin<br>
pipwin install PyAudio<br>
(sudo) python -m pip install grpcio<br>
python -m pip install grpcio-tools<br><br>

(1) Il faut tout d'abord modifier le fichier CSV "**liste_eleve**", y mettre son **prénom**, **nom** et un **code** (code qui va permettre de se connecter).<br><br>

(2) Ensuite, il est nécessaire d'ajouter une photo dans le dossier **known_faces** (qui va permettre de reconnaître l'élève), dont le nom de la photo devra être le **prénom** renseigné dans le fichier CSV.<br><br>

(3) Dans le répertoire du projet, lancez la commande : <br>
**python -m grpc_tools.protoc -I../NOM_DOSSIER --python_out=. --grpc_python_out=. proto/communication.proto**<br>
Cette commande va permettre de créer les fichiers nécessaire à la communication application mobile-logiciel PC.<br><br>

(4) Lancez le logiciel PC avec la commande : **python main.py**

(5) Lancez l'application mobile, connectez-vous, puis suivez les instructions. Une fois les instructions de l'application faites, le serveur va à son tour détecter si ce dernier est apte à passer l'examen.


<br><br>


### Autheurs
- Michel KADDOUH
- Alexandre GOUI

