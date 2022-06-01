# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:11:25 2022

@author: xavie
"""



import mido  
import time  
 

#port dispo
port1 = mido.get_output_names()
port = mido.open_output(port1[0])
 

mid = mido.MidiFile('test1.mid')
 
# affiche chemin fichier Midi + son type + nb de pistes + nb de messages dans fichier
print("=>", mid, "...\n... ...")
 
# calcul + affiche la durée de lecture du fichier Midi en h:m:s
print("=> Durée de lecture =", time.strftime('%Hh:%Mm:%Ss', time.gmtime(mid.length)))
print("=> Lecture en cours...")
 
for msg in mid.play():  # boucle de lecture du fichier Midi
    port.send(msg)      # envoi fichier Midi port MidO-OUT vers IN QS-M2 Qsynth/FS
 
port.close()  # ferme proprement le port Midi
print("=> Fichier MIDI lu... ARRÊT !")