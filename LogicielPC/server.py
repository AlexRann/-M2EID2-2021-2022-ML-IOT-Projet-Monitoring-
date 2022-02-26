# -*- coding: utf-8 -*-
"""
Fichier qui gère la communication entre l'application mobile et le serveur Python
@author: - Alexandre GOUI
         - Michel Kaddouh
"""



"""
python -m grpc_tools.protoc -I../Projet_Monitoring --python_out=. --grpc_python_out=. proto/communication.proto
"""

from concurrent import futures
import grpc
import logging
import base64
import pandas as pd

import proto.communication_pb2 as communication_pb2
import proto.communication_pb2_grpc as communication_pb2_grpc



"""
Les messages du client au serveur sont du type :
        
- (string) check_connexion : variable gardée pour la communication serveur à client.
    Vaut 'good' ou 'bad', dépend de la présence du CODE_ETUDIANT fourni par le client
    
- (string) code_etudiant : code étudiant fourni par le client, permet d'identifier les messages des clients.
    
- (string) type_message : variable servant à marquer le début et la fin d'une communication client-serveur.
    Vaut 'Connexion', 'Déconnexion' ou 'Data'.
    
- (string) msg_accel : variable permettant d'informer le serveur si l'élève à bouger la tête dans quelle direction.
    Vaut 'Haut', 'Bas', 'Droite' ou 'Gauche'
    
- (string) img : variable permettant le partage de photo (prise automatiquement) du client au serveur.
    Image au format String Base64, va être décodé pour reconstruire une image, puis sauvegardée pour y être analysée
"""



# On récupère le CSV qui contient le nom de l'étudiant, 
inscrits_exam = pd.read_csv ('liste_eleve.csv')
codes_etudiant = inscrits_exam['CODE']





"""
    Paramètres
        img_data : image au format String Base64
        i : Integer pour le nom de la photo sauvegardée
"""
def base64_to_image (img_data, i) :
    
    if len(i) > 0 :
        name_file = "photo_bureau/image_tel" + str(i) + ".jpg"
    else :
        name_file = "image_tel.jpg"
    
    with open(name_file, "wb") as fh:
        fh.write( base64.decodebytes(img_data) )



"""
    Définition d'une classe gRPC
"""
class Communication(communication_pb2_grpc.CommunicationServicer):

    def SendComm(self, request, context):
        img_recu = ""

        # Si le code étudiant est présent parmi la liste des codes étudiants, alors c'est good, sinon c'est bad
        check_code_etudiant = "bad"
        if codes_etudiant.eq( request.code_etudiant ).any() :
            check_code_etudiant = "good"

            # Si on recoit une image, alors on la traite
            # On récupère l'image au format String Base64 et on la transforme et stocke au format JPG
            if len(request.img) > 0 :
                img_recu = "Recu"
                print ( "[", request.code_etudiant, request.dateTime, "]", request.type_message,request.msg_accel, "img:"+img_recu )
                                    
                # Si on reçoit la photo du bureau de la phase photocole, on la garde
                if request.type_message == "PhotoBureau" :
                    base64_to_image( str.encode(request.img), "_bureau_"+str(request.code_etudiant)+"_"+str(request.dateTime) )
                # Sinon on peut réécrire sur la même photo
                else :
                    base64_to_image( str.encode(request.img), "" )
                    
                
            # Sinon, on n'a pas reçu d'image
            else :
                print ( "[", request.code_etudiant, request.dateTime, "]", request.type_message,request.msg_accel )


        # Sinon, le code étudiant est faux
        else :
            print ( "[", request.code_etudiant, request.dateTime, "]", "Code étudiant éroné ou non présent !" )
            
        if request.msg_accel != "" :
            with open('data.txt', 'w') as f:
                f.write( str(request.code_etudiant) + "," + str(request.msg_accel) )
        
        return communication_pb2.ReplyComm( check_connexion = check_code_etudiant,
                                           type_message = request.type_message,
                                           msg_accel = request.msg_accel,
                                           img = request.img )





"""
    Définition d'un serveur type gRPC (localhost, 50051)
"""
def server () :
    with open('data.txt', 'w') as f:
        f.write('')
        
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_CommunicationServicer_to_server(Communication(), server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    

def connexion():
    logging.basicConfig()
    server()






