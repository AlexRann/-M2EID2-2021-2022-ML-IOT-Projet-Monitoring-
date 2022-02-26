# -*- coding: utf-8 -*-
"""
Fichier qui gère le micro

@author: - Alexandre GOUI
         - Michel Kaddouh
"""

import speech_recognition as sr
import communication
from datetime import datetime


# Reprise du tutoriel de
# http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/projets/technique.html
# https://www.datacorner.fr/audio-recog/

# intervention    
class Reco_Voix:
    def __init__(self):
        # Compteur pour les audios enregistré
        self.__cpt = 0
        
        self.r = sr.Recognizer()
        
        # Microphone que l'on va utiliser
        self.mic = sr.Microphone()
        # Mot que l'on considére comme mots triches
        self.mot_triche = ['RÉPONSE', 'REPONSE', 'QUESTION', 'RÉP', 'REP', 'QUEST', 'COCHER']
# fin intervention
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source, duration=5)
    
    
# intervention    
    def rajouter_mot_triche(self,liste_mot) :
        """
        Fonction pour ajouter les mots que l'on suspecte être des mots triches
        l'orsque la machine détectera un de ses mots, il enregistre l'audio

        Parameters
        ----------
        liste_mot : list
            Liste de mot que l'on veut ajouter.

        Returns
        -------
        None.

        """
        maj = [string.upper() for string in liste_mot]
        self.mot_triche += maj
        
    def enregistrer_voix(self,audio):
        with open("./audio/audio_file_"+str(datetime.now().strftime("%d_%m_%Y_%H_%M"))+".wav", "wb") as file:
            file.write(audio.get_wav_data())
        self.__cpt += 1
            
    def test_voix(self):
        """
        Ecoute le son du micro et enrgistre l'audio si un des mots triche à été
        reconnu

        Returns
        -------
        None.

        """
# fin intervention
        with self.mic as source:
          audio = self.r.listen(source)
          try:
            son = self.r.recognize_google(audio, language="fr-FR")
          except :
            son = ''

          if len(son) != 0:
############################### FIN DU CODE REPRIS ###############################
              if  any(mot in son.upper() for mot in self.mot_triche):
                  communication.parole(False)
                  self.enregistrer_voix(audio)

    def routine_voix(self) :
        """
        Défini la routine que fait la caméra pour la detection vocale.
        C'est la fonction que l'on va lancer avec un thread.

        Returns
        -------
        None.

        """
        while 1 :
            self.test_voix()

        
