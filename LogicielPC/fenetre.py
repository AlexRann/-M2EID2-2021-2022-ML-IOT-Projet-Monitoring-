# -*- coding: utf-8 -*-

# Reprise du code de
# https://stackoverflow.com/questions/40809729/can-python-get-the-screen-shot-of-a-specific-window

import pygetwindow
import time
import pyautogui

# intervention

class Fenetre : 
    __ne_pas_fermer = [ '', '','Paramètres','Paramètres','','','','','Microsoft Text Input Application','Program Manager']

    def __init__(self):
        self.__cpt = 0
        
    def tout_fermer(self):
        screen = pygetwindow.getAllTitles()
        #On suppose que le partiel se fait sur internet
        matches = [match for match in screen if "Spyder" in match or "Mozilla" in match or "Chrome" in match]

        supr = [x for x in screen if x not in matches and x not in self.__ne_pas_fermer]


        for new_window in supr :
            my = pygetwindow.getWindowsWithTitle(new_window)[0]
            my.close()
        
        time.sleep(0.5)
        self.fenetre = pygetwindow.getAllTitles()
        time.sleep(0.5)
        
        
    def verif(self) :
# fin intervention
        z2 = pygetwindow.getAllTitles()
        
        z3 = [x for x in z2 if x not in self.fenetre]
        
        if z3 != [] :
            for new_window in z3 :
                my = pygetwindow.getWindowsWithTitle(new_window)[0]
            
                my.activate()
                time.sleep(0.5)

                # save screenshot
                p = pyautogui.screenshot()
                p.save('./screen/screen' + str(self.__cpt) + '.png')
                self.__cpt += 1
                
############################### FIN DU CODE REPRIS ###############################
                # ne pas fermer la page internet (la ou se trouve le partiel)
                if not ("Mozilla".upper() in new_window.upper() or "Chrome".upper() in new_window.upper()) :
                    time.sleep(0.5)
                    my.close()
