# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:35:41 2022

@author: xavie
"""


import mido    
from mido import Message, MidiFile, MidiTrack  
import time    
 
mid = MidiFile()          # Nous pouvons créer un nouveau fichier en appelant MidiFile
track = MidiTrack()       # sans l’argument du nom de fichier. Le fichier peut ensuite
mid.tracks.append(track)  # être enregistré à la fin en appelant la méthode save()
 

note = [28,28,28,24,28,31,43,43,24,24,43,43,40,40,33,33,35,35,34,33,33,43,28,31,21,29,31,28,28,24,26,35] #note
rythme = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0] #durée des notes
hauteur = [0,-12,0,+12,0]  # choix des octaves à jouer, 12 = 1 octave et 0 = original
 
x = 0  #  initialisation index x lecture de gauche à droite liste "hauteur"
for i in hauteur:  # boucle octave à jouer par rapport aux notes d'origine
    delta = hauteur[x]  # nb d'octaves à ajouter ou soustraire exprimé par tranche de 12 notes
    print("   => HAUTEUR =", delta,"notes...")  # affiche nb notes en + ou -
    x = x +1  # incrémentation index x pour hauteur octave (de 0 à nb dans liste "hauteur")
 
    y = 0 
    for j in note:  # boucle notes à jouer dans noctn (notes partition)
        track.append(Message('program_change', program=64, time=0))  # n. program=instrument
        track.append(Message('note_on', note = note[y] +delta, velocity = 100, time = 32))
        print("Nocturne note #", note[y],"- Durée =", (rythme[y]), "- time =", int(256 *rythme[y]))
        track.append(Message('note_off', notea = note[y] +delta, velocity = 67, time = int(256 *rythme[y])))
        y = y +1  # incrémentation index y pour couple note/durée (de 0 à nb dans liste "noctn")
 
 
mid.save('MIDO_Write-Nocturne-Composition-File.mid')  # enregistre le tout dans ce fichier Midi
print("=> Fichier MIDI sauvegardé", mid, "...")  # affiche info fichier Midi
print("C'EST FINI !")