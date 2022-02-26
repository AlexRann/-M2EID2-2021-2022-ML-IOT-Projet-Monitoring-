# -*- coding: utf-8 -*-
"""
Main du projet, le lancer pour commencer le système anti-triche
@author: - Alexandre GOUI
         - Michel Kaddouh
"""

import camera
import communication
import micro
import server
import cv2
import time
from threading import Thread
import pandas as pd

serveur = Thread(target = server.connexion)
serveur.start()

# On récupére les données des élèves qui peuvent se connecter
inscrits_exam = pd.read_csv ('liste_eleve.csv', index_col ="CODE")
codes_etudiant = pd.read_csv ('liste_eleve.csv')['CODE']


nom = ''
# on attend que l'élève se connecte
while nom == '' :
    try :
        code_recu = str(pd.read_table("data.txt", sep = ',',header=None).values[0][0])
    except:
        code_recu = '0'
    try:
        donne = inscrits_exam.loc[code_recu]
        nom = donne.values[0]
        prenom = donne.values[1]
    except :
        nom = ''
                
#__________________________________________________________________

# Si voix = True l'ordinateur parlera au lieu d'envoyer des pop-ups
# voix = True
voix = False

# Initialisation

communication.Initialisation(voix)
video_capture = cv2.VideoCapture(0)
eleve = camera.Camera(code_recu,prenom,nom,voix)
voix_mic = micro.Reco_Voix()
bonjour = 1

# Initialisation des Threads
test_voix = Thread(target = voix_mic.routine_voix)
test_mouvement = Thread(target = eleve.detect_mouvement, args =(video_capture,))
test_cam = Thread(target = eleve.routine_camera, args =(video_capture,))
test_objet = Thread(target = eleve.detect_obj_cam, args =(video_capture,))


#__________________________________________________________________

       
communication.debut(voix)
time.sleep(1)

# Initialisation reconnaitre la personne
# Tant que je n'ai pas dit bonjour, je ne passe pas à l'étape suivante et je continue
# de tester la personne en face de la caméra.
while bonjour:
        # Je teste pendant 2 seconde si l'élève n'est pas reconnue
        eleve.test_personne_cam(video_capture, time.time(), 2)
                
        # s'il est reconnue, je dis bonjour et je sors de la boucle
        if eleve.user.upper() in eleve.name: 
            communication.dire_bonjour(eleve.user.upper(), voix)
            bonjour = 0
                    
        # Sinon on lui demande de recadrer sa caméra
        else : 
            communication.mauvaise_personne(eleve.user.upper(), voix)
            communication.recadrer_camera(voix)

# Lancement des Threads
test_voix.start()
test_cam.start()
test_mouvement.start()
test_objet.start()

while 1 :
    1

