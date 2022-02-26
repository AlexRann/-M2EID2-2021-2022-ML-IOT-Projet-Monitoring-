# -*- coding: utf-8 -*-
"""
Fichier qui gère la caméra.
Initialise un eleve à partir d'un code recu dans le main.

Elle contient la détection de visage, d'objet et de mouvement par
sosutraction d'image.

@author: - Alexandre GOUI
         - Michel Kaddouh
"""

import face_recognition
import cv2
import numpy as np
import os
import time
import communication
from datetime import datetime
import re

class Camera:
    def __init__(self,code, prenom,nom, voix):
        # Compteur pour screens
        self.prenom = prenom
        self.nom = nom
        self.user = nom + " " + prenom
        # path de la photo de la personne
        self.path = "./known_faces/" + prenom.lower()
        # Récupération de la photo et encodage du visage pour tester plus tard
        if os.path.isfile(self.path+".jpeg"):
            image = face_recognition.load_image_file(self.path+".jpeg")
        elif os.path.isfile(self.path+".png"):
            image = face_recognition.load_image_file(self.path+".png")
        elif os.path.isfile(self.path+".jpg"):
            image = face_recognition.load_image_file(self.path+".jpg")
        self.known_face_encodings = face_recognition.face_encodings(np.array(image))
        
        # Nombre de portable, téléphone et ordinateur
        self.nb_tel_person_obj = 0
        self.nb_tel_tel = 0
        self.nb_tel_ordi = 0
        
        # Lien de l'mage a recu par le telephone
        # A l'initialisation un fond noir
        self.path_img = "./image_tel.jpg"
        
        # Modèle préentrainé pour la detection d'objet
        net = cv2.dnn_DetectionModel('./model/frozen_inference_graph.pb', './model/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)
        self.net = net
        
        # autre variable
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True  
        self.voix = voix
        self.name = []
        self.nb_tel = 0
        self.nb_ordi = 0
        self.nb_person = 1
        self.nb_person_obj = 1
        self.code = code
        self.position = ''

    def photo(self,frame, path) :
        """
        Sauvegarde une photo dans un dossier.

        Parameters
        ----------
        frame : array
            Image que l'on veut sauvegarder.
        path : string
            Endroit ou l'on sauvegarde la variable frame.

        Returns
        -------
        None.

        """
        cv2.imwrite(path +'photo_'+str(datetime.now().strftime("%d_%m_%Y_%H_%M"))+'.png', frame)

   
    def nb_visage(self,traited_frame) :
        """
        Localise et compte le nombre de visage sur une image prétraitée donné en parametre.

        Stocke le nombre de personne et la localisation des visage trouvées
        dans une variable.
        
        Parameters
        ----------
        traited_frame : array
            Image traité par la fonction trait_frame.

        Returns
        -------
        None.

        """
        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(traited_frame)
            self.nb_person = len(self.face_locations)
            
# Reprise du code de
# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py            
    def trait_frame(self, frame) :
        """
        Traite une image : réduit la taille et la dimension 

        Parameters
        ----------
        frame : array
            image que l'on souhaite traitée.

        Returns
        -------
        rgb_small_frame : array
            image traitée.

        """
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        return rgb_small_frame
    
    def reconaissance(self,traited_frame) :
        """
        Prends la même image que celle de la fonction nb_visage et compare
        les visages trouvées avec celui stocker dans le dossier.
        
        Stocke le nom de la personne si elle a été reconnue dans la variable name
        sinon stocke 'unknow'.

        Parameters
        ----------
        traited_frame : array
            Image traité par la fonction trait_frame.

        Returns
        -------
        None.

        """
    
        self.name = []
        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_encodings = face_recognition.face_encodings(traited_frame, self.face_locations)
    
            for face_encoding in face_encodings:
                name = "unknow"
                # See if the face is a match for the known face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
# intervention    
                if face_distances < 0.55:
                    name = self.user
                self.name.append(name.upper())
        self.process_this_frame = not self.process_this_frame

# fin intervention
############################### FIN DU CODE REPRIS ###############################
    def test_personne(self, frame, test) :
        """
        Traite l'image donnée et compte le nombre de personne. 

        Parameters
        ----------
        frame : array
            image que l'on va traitée.
        test : bool
            si True, test le nombre de personne et :
                - Prend en photo s'il y a plus d'une personne.
                - S'il y a une personne regarde si c'est la personne qui passe le 
                test.

        Returns
        -------
        None.

        """
        rgb_frame = self.trait_frame(frame)
        self.nb_visage(rgb_frame)
        if test : 
            if self.nb_person == 1 :
                self.reconaissance(rgb_frame)
                
            elif self.nb_person > 1 or self.nb_person_obj > 1 :
                self.photo(frame, './photo/nb_pers/')
                communication.plus_person(self.voix)            
    
    
    def test_personne_cam (self, video, temps, temps_test, test = True) :
        """
        Va essayer de reconnaitre la personne image par image pendant 
        temps_test secondes ou jusq'a qu'il a reconnu la personne.

        Parameters
        ----------
        video : cv2.VideoCapture
            Source d'image que l'on va traitée, ici video de notre caméra.
        temps : int
            le temps du début du test.
        temps_test : int
            le temps (en seconde) que l'on va essayer de reconnaitre la personne.
        test : bool, optional
            si True :
                - S'il ne reconnait personne, prend une photo du moment et 
                prévient la personne.
                - S'il ne reconnait pas la personne, prend une photo du moment et 
                prévient la personne.
            The default is True.

        Returns
        -------
        None.

        """
        # On va tester tant que le temps définit n'est pas écoulé ou qu'on a toujours pas reconnu la personne
        while (time.time() - temps < temps_test) and self.user.upper() not in self.name :
            _, frame = video.read()
            self.test_personne(frame, test)
          
        if test == True :
            # Si personne n'est reconnue, on prend une photo et on demande a la personne de bien
            # se recadrer
            if self.nb_person == 0 and self.nb_person_obj == 0 :
                self.photo(frame, './photo/0_reco/')
                communication.personne(self.voix)
                communication.recadrer_camera(self.voix)
            
            # Si l'eleve n'est pas reconnue, on prend une photo et on demande a la personne de bien
            # se recadrer
            elif self.user.upper() not in self.name :
                self.photo(frame, './photo/pas_reco/')
                communication.mauvaise_personne(self.user.upper(),self.voix)
                communication.recadrer_camera(self.voix)
                

    def routine_camera(self, video) :
        """
        Défini la routine que fait la caméra pour la reconnaissance de personne.
        C'est la fonction que l'on va lancer avec un thread.
        Si le nombre de personne est différent de 1, ou que 2 minutes se sont
        écoulées on test la personne pour voir si elle est la et que c'est la
        bonne personne

        Parameters
        ----------
        video : cv2.VideoCapture
            Source d'image que l'on va traitée, ici video de notre caméra.

        Returns
        -------
        None.

        """
        temps = time.time()
        sec = time.time()
        while True:
            # Fait des tests toutes les secondes
            if time.time() - sec > 1 :
                with open('data.txt', 'r') as f:
                    message = f.read()
                
                try : 
                    recu = re.split(',', message)
                except :
                    recu = ['']
                
                try : 
                    self.position = recu[1]
                except :
                    self.position = ''
                    
                self.test_personne_cam(video, time.time(), 1, False)
                
                    
                # Si le nombre de personne est != 1
                # Ou que 2 minutes se sont écoulées je teste la caméra             
                if (self.nb_person != 1 and self.nb_person_obj != 1 and self.nb_ordi == 0) or time.time() - temps > 120 :
                    
                # Eviter que l'élève met sa tête dans un telephone/ordinateur et qu'un autre élève passe l'examen à la place
                # Impossible a faire avec le proto car toujours un téléphone
                # if (self.nb_person != 1 and self.nb_person_obj != 1 and (self.nb_tel == 0 and self.nb_ordi == 0)) or time.time() - temps < 120 :
                    
                    self.name = []
                    while self.user.upper() not in self.name :
                        self.test_personne_cam(video, time.time(), 2)
                        
                    if time.time() - temps > 120 :
                        temps = time.time()
                
                
                # On centralise les commandes vocales pour éviter le chevauchement entre les Threads
                if self.nb_tel > 1 :
                    communication.tel(self.voix)
                    
                if self.nb_ordi > 0 :
                    communication.ordi(self.voix)
                
                
                if self.position.upper() :
                    if self.position.upper().split()[0] == 'GAUCHE' or\
                        self.position.upper().split()[0] == 'DROITE' or\
                            self.position.upper().split()[0] == 'HAUT' or\
                                self.position.upper().split()[0] == 'BAS' or\
                                    self.position.upper().split()[0] == 'HAUT-GAUCHE' or\
                                        self.position.upper().split()[0] == 'HAUT-DROITE' or\
                                            self.position.upper().split()[0] == 'BAS-GAUCHE' or\
                                                self.position.upper().split()[0] == 'BAS-DROITE' :
                        img = cv2.imread(self.path_img)
                        self.detect_obj_img(img)
                        communication.regarder(self.position, self.voix)
                        while self.nb_tel_person_obj > 0 or self.nb_tel_tel > 0 or self.nb_tel_ordi > 0 :
                           
                            if self.nb_tel_person_obj > 0:
                                try :
                                    self.photo(img, './photo/nb_reco/')
                                    communication.plus_person(self.voix)
                                except :
                                    print()
            
                            if self.nb_tel_tel > 0 :
                                try :
                                    self.photo(img, './photo/telephone/')
                                    communication.tel_orient(self.position, self.voix)
                                except :
                                    print ()
                                
                            if self.nb_tel_ordi > 1 :
                                try :
                                    self.photo(img, './photo/ordinateur/')
                                    communication.ordi_orient(self.position, self.voix)
                                except :
                                    print()
                                    
                            try :
                                img = cv2.imread(self.path_img)
                                time.sleep(1)
                                self.detect_obj_img(img)
                            except :
                                print()
                        communication.reprise(self.voix) 
                    sec = time.time()

# Reprise du code de
# https://github.com/L42Project/Tutoriels/blob/master/OpenCV/tutoriel26/camera.py
    def detect_mouvement (self, video):
        """
        Défini la routine que fait la caméra pour la detection de mouvement.
        C'est la fonction que l'on va lancer avec un thread.
        

        Parameters
        ----------
        video : cv2.VideoCapture
            Source d'image que l'on va traitée, ici video de notre caméra.

        Returns
        -------
        None.

        """
        sec = time.time()
        while 1 :
            # Fait des tests toutes les secondes
            if time.time() - sec > 1 :
                _, frame =video.read()
                frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame=cv2.GaussianBlur(frame, (11, 11), 0)
                i = 0
                image = 0
                nbr_img = 0
                debut = time.time()
                # On compte le nombre de mouvement pendant 3 seconde
                while time.time() - debut < 3:
                    _, photo=video.read()
                    gray=cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
                    gray_blur=cv2.GaussianBlur(gray, (11, 11), 0)
                    # On fait la différence des images frame et photo
                    mask=cv2.absdiff(frame, gray_blur)
                    mask=cv2.threshold(mask, 20, 255, cv2.THRESH_BINARY)[1]
                    nbr_pixel=int(np.sum(mask)/255)
    # intervention    
                    nbr_img += 1
                    # Si le nombre de pixel différent et supérieur à 15000 on incrémente une variable
                    if nbr_pixel>15000:
                        i += 1
    
                    # Si le nombre de pixel ne change pas du tout (en prenan en compte le bruit)
                    # On peut supposer que l'élève à accroché une image
                    if nbr_pixel < 100:
                        image += 1
                        
                    frame=gray_blur
                    
                # Si le nombre de mouvement est supérieur au nombre d'image (qu'il a bougé sur chaque image) on prend une photo.
                if i >= nbr_img :
                    self.photo(photo, './photo/mouvement/')
                
                if image >= nbr_img :
                    self.photo(photo, './photo/pas_mouvement/')
# fin intervention
                sec = time.time()
############################### FIN DU CODE REPRIS ###############################

    def detect_obj_cam (self, video):
        """
        Défini la routine que fait la caméra pour la detection d'objet.
        C'est la fonction que l'on va lancer avec un thread.
        
        Stocke le nombre d'objet vu dans des variables.
        Parameters
        ----------
        video : cv2.VideoCapture
            Source d'image que l'on va traitée, ici video de notre caméra.

        Returns
        -------
        None.

        """
        sec = time.time()
        while True:
            # Fait des tests toutes les secondes
            if time.time() - sec > 1 :
                temps = time.time()
                classIds = []
                classTest = []
                # On teste pendant 2 seconde
                while time.time() - temps < 2 :
                    _, img_test = video.read()
                    classTest, _, _ = self.net.detect(img_test, confThreshold=0.55)
                    # On va prendre le moment ou l'algorithme a reconnue le plus d'objet
                    if len(classTest) > len(classIds):
                        classIds = classTest
                        img = img_test
                    
                # 63 = laptop
                # 76 = cell phonr
                # 0 = person
                if len(classIds) != 0:
                    classIds = np.array(classIds) - 1
                    classIds = classIds.tolist()
                    self.nb_person_obj = classIds.count(0)
                    self.nb_tel = classIds.count(76)
                    self.nb_ordi = classIds.count(63)
                    
                # S'il ne reconnait rien prends une photo
                else :
                    self.photo(img, './photo/0_reco/')
    
                    
                if self.nb_tel > 1 :
                    self.photo(img, './photo/telephone/')
                    
                if self.nb_ordi > 0 :
                    self.photo(img, './photo/ordinateur/')
                
                sec = time.time()

            
    def detect_obj_img (self, img):
        """
        Detection d'objet a partir d'une image.
        C'est la fonction que l'on va lancer pour detecter les images recu par le telephone.
       
        Parameters
        ----------
        img : numpy.ndarray
            image que l'on va traitée, ici l'image recu de la camera frontale.

        Returns
        -------
        None.

        """
        classIds = []
        try :
            classIds, _, _ = self.net.detect(img, confThreshold=0.55)
        except :
            classIds = []
        # 63 = laptop
        # 76 = cell phone
        # 0 = person
        if len(classIds) != 0:
            classIds = np.array(classIds) - 1
            classIds = classIds.tolist()
            self.nb_tel_person_obj = classIds.count(0)
            self.nb_tel_tel = classIds.count(76)
            self.nb_tel_ordi = classIds.count(63)