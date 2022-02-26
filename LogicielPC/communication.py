# -*- coding: utf-8 -*-
"""
Fichier qui gère la communication entre le système et celui qui passe l'examen.

On peut communiquer par pop-ups ou par synthèse vocale.

@author: - Alexandre GOUI
         - Michel Kaddouh
"""
from win32com.client import Dispatch
from tkinter import *
from threading import Thread


def lancer_fenetre (texte, color) :
    """
    Créer un pop-up qui reste au premier plan pendant 2 secondes pour communiquer
    avec l'utilisateur.

    Parameters
    ----------
    texte : string
        texte que l'on veut afficher dans notre pop-up.
    color : string
        couleur de notre pop-up.

    Returns
    -------
    None.

    """
    # Création d'une fenêtre avec la classe Tk :
    fenetre = Tk()
    fenetre.after(5000, lambda: fenetre.destroy())
    fenetre.wm_attributes("-topmost", 1)
    fenetre.configure(bg=color)
    fenetre.overrideredirect(1)
    # Ajout d'un texte dans la fenêtre :
    texte1 = Label (fenetre, text = texte, font=("Courier", 20))
    texte1.config(bg=color)
    texte1.pack()
    button = Button(fenetre, text = 'Compris !', command=fenetre.destroy, font=("Courier", 20))
    button.pack()
    # Affichage de la fenêtre créée :
    fenetre.mainloop()


def pas_mouvement(voix) :
    """
    affiche ou lit le texte : Aucun mouvement détecté sur une trop longue période, hochez votre tête

    Parameters
    ----------
    voix : bool
        si True : lit le texte à l'utilisateur, sinon affiche une pop-up.

    Returns
    -------
    None.

    """
    texte = "Aucun mouvement détecté sur une trop longue période, hochez votre tête"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'orange',))
        affiche_fenetre.start()    

def Initialisation (voix ) :
    texte = "Bonjour, initialisation en cours, veuillez patienter."
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'green',))
        affiche_fenetre.start()


def reprise (voix ):
    texte = "Vous pouvez reprendre votre examen"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'green',))
        affiche_fenetre.start()

def debut (voix ):
    texte = "Nous allons commencez l'examen. Mettez vous face a votre caméra"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'green',))
        affiche_fenetre.start()
        
def regarder(orientation, voix ):
    texte = "Regardez vers la direction : " + orientation + " s'il vous plaît"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'orange',))
        affiche_fenetre.start()
        
def tel_orient(orientation, voix ):
    texte = "Un telephone a été vu à " + orientation + " , veuillez le retirer s'il vous plaît"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'red',))
        affiche_fenetre.start()
        
def ordi_orient(orientation, voix ):
    texte = "Un ordinateur a été vu à " + orientation + " , veuillez le retirer s'il vous plaît"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'red',))
        affiche_fenetre.start()
        
def plus_person(voix ):
    texte = "Une seule personne autorisée pendant l'examen"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'red',))
        affiche_fenetre.start()
        
def mauvaise_personne(name, voix ):
    texte = name + " n'est pas reconnu"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'red',))
        affiche_fenetre.start()
        
def recadrer_camera(voix ):
    texte = "Veuillez recadrer votre camera"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'orange',))
        affiche_fenetre.start()
        
def merci(voix ):
    texte = "Merci"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'green',))
        affiche_fenetre.start()
        
def au_revoir(voix ):
    texte = "au revoir"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'green',))
        affiche_fenetre.start()
        
def face_camera(voix ):
    texte = "Veuillez vous mettre en face de votre camera"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'orange',))
        affiche_fenetre.start()
        
def dire_bonjour(name, voix ):
    texte = "Bienvenue, " + name + " vous pouvez commencer l'examen"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'green',))
        affiche_fenetre.start()
        
def personne(voix ):
    texte = "Personne n'est reconnue devant la caméra"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'orange',))
        affiche_fenetre.start()
        
def tel(voix ):
    texte = "Un telephone est détecté, veuillez le retirer"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'red',))
        affiche_fenetre.start()
        
def ordi(voix ):
    texte = "Un ordinateur est détecté, veuillez le retirer"
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'red',))
        affiche_fenetre.start()
        
def parole():
    texte = "Eviter de trop parler durant l'examen"
    affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,'orange',))
    affiche_fenetre.start()

def autre(texte, couleur, voix ):
    if voix : 
        Dispatch("SAPI.SpVoice").Speak(texte)
    else :
        affiche_fenetre = Thread(target = lancer_fenetre, args =(texte,couleur,))
        affiche_fenetre.start()
        