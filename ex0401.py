#!/usr/bin/env python3
# coding: utf8

# Nom           : ex0401.py
# Rôle          : Code source de l'exercice 01 du TP4 
# Auteur        : Ronan LOSSOUARN
# Date          : 15/08/2022
# Licence       : L1 Outils Collaboratifs

# SYNOPSIS
# ./ex0401.py

# DESCRIPTION
# Le programme affiche toutes les données EXIF d'une image.
# Il permet également d'afficher la position de l'image sur une carte
# Enfin, il est possible de changer certaines données EXIF

# Fonctions importées
import streamlit as st
from PIL import Image as imagePIL
from exif import Image as imageExif
import pandas as pd

# objectif : change tous les attributs de date d'une image
# @param image -> une image ouverte avec le module exif
def changeDate(image):
    # saisies des nouvelles valeurs
    date = st.date_input('Nouvelle date')
    time = st.time_input('Nouvelle heure')
    datetime = str(date) + " " + str(time) # concatène la date et l'heure

    clicked = st.button("Modifier", key = 1) # bouton pour affirmer la modifcation

    if clicked:  
        image.set('datetime', datetime)
        image.set('datetime_digitized', datetime)
        image.set('datetime_original', datetime)

        st.write(f"Nouvelle horodatage :") # affiche le changement
        st.info(f"{image.get('datetime', 'Unknown')}")

    return datetime

# objectif : change la valeur d'un attribut de type String d'une image
# @param image -> une image ouverte avec le module exif
def changeString(attribut, image):
    # saisie de la nouvelle valeur
    value = st.text_input("Modification " + attribut)

    clicked = st.button("Modifier", key = 3) # bouton pour affirmer la modifcation

    if clicked: 
        image.set(attribut, value)

         # affiche le changement 
        st.write(f"Nouvelle valeur {attribut} :")
        st.info(f"{image.get(attribut, 'Unknown')}")

    return value

# objectif : change les coordonnées d'une image
# @param image -> une image ouverte avec le module exif
def changeGps(image):
    # saisies des nouvelles valeurs
    latRef = st.selectbox("Latitude : ", ('N', 'S'))
    latDD = st.number_input('Latitude Degrés', 0.00, 90.00)
    latMM = st.number_input('Latitude Minutes', 0.00, 60.00)
    latSS = st.number_input('Latitude Secondes', 0.00 ,60.00)

    lngRef = st.selectbox("Longitute : ", ('W', 'E'))
    lngDD = st.number_input('Longitude Degrés', 0.00, 180.00)
    lngMM = st.number_input('Longitude Minutes', 0.00, 60.00)
    lngSS = st.number_input('Longitude Secondes', 0.00, 60.00)

    clicked = st.button("Modifier") # bouton pour affirmer la modifcation

    if clicked:
        image.gps_latitude = (latDD, latMM, latSS)
        image.gps_latitude_ref = latRef
        image.gps_longitude = (lngDD, lngMM, lngSS)
        image.gps_longitude_ref = lngRef

        st.write(f"Nouvelle valeur coodonnées :")  # affiche le changement 
        st.info(f"Latitude: {image.get('gps_latitude')} {image.get('gps_latitude_ref')}")
        st.info(f"Longitude: {image.get('gps_longitude')} {image.get('gps_longitude_ref')}")

    return (latDD, latMM, latSS, latRef, lngDD, lngMM, lngSS, lngRef)

# objectif : convertie des coordonnées degrés minutes secondes en degrés décimales
# @param coordinates -> l'attribut changé
# @param image -> une image ouverte avec le module exif
# source : https://auth0.com/blog/read-edit-exif-metadata-in-photos-with-python/
def dmsCoordinatesToDdCoordinates(coordinates, coordinatesRef):
    decimalDegrees = coordinates[0] + \
                      coordinates[1] / 60 + \
                      coordinates[2] / 3600
    if coordinatesRef == "S" or coordinatesRef == "W":
        decimalDegrees = -decimalDegrees
    return decimalDegrees

if __name__ == "__main__":
    st.title("Exercice 4.1")

    # ouvre le fichier avec le module PIL pour l'afficher
    imageP = imagePIL.open('DSCN0010.jpg')
    st.image(imageP, caption='Source : https://github.com/ianare/')

    # ouvre le fichier et initialise la classe d'interface exif de l'image
    with open("DSCN0010.jpg", "rb") as imageFile:
        imageE = imageExif(imageFile)

    # initialise les coordonnées de ma position
    imageE.gps_latitude = (48, 35, 69.9)
    imageE.gps_latitude_ref = 'N'
    imageE.gps_longitude = (7, 43, 10.41)
    imageE.gps_longitude_ref = 'E'

    # affiche toutes les données exif de l'image
    imageDirs = dir(imageE)
    st.write(f"La photo contient {len(imageDirs)} métadonnées : ")
    for attribut in imageDirs :
        # evite les attributs vide
        if "unknown" in attribut or imageE.get(attribut, 'Unknown') == "Unknown":
            continue 
        st.write(f"{attribut} :")
        st.info(f"{imageE.get(attribut, 'Unknown')}")

    # menu déroulant pour sélectionner l'attribut à changer
    attribut = st.selectbox(
        'Quel attribut voulez-vous changer?',
        (None, 'datetime', 'lens_make', 'lens_model', 'make', 'model', 'software', 'gps'))

    if attribut:
        st.write(attribut + " :")
        st.info(f"{imageE.get(attribut, 'Unknown')}")
        # sélection de la fonction de changement de valeur
        if attribut == 'datetime':
            changeDate(imageE)
        elif attribut == 'lens_make':
            changeString(attribut, imageE)
        elif attribut == 'lens_model':
            changeString(attribut, imageE)
        elif attribut == 'make':
            changeString(attribut, imageE)
        elif attribut == 'model':
            changeString(attribut, imageE)
        elif attribut == 'software':
            changeString(attribut, imageE)
        elif attribut == 'gps':
            changeGps(imageE)
        else :
            None

    # point de toutes la localisations de la carte
    data = pd.DataFrame({
        'awesome cities' : ['Localisation de la photo', 'Longvic', 'Annecy', 'Grenoble',
            'Versailles', 'Niamey', 'N\'Djamena', 'Djibouti',
            'Abu Dhabi', 'Mafraq', 'Washington DC', 'Puebla'],
        'lat' : [dmsCoordinatesToDdCoordinates(imageE.get('gps_latitude'), imageE.get('gps_latitude_ref')),
            47.285188, 45.900191, 45.188270, 48.788486,
            13.678118, 12.124878, 11.803042, 24.460458,
            32.354489, 38.916282, 19.055769
            ],
        'lon' : [dmsCoordinatesToDdCoordinates(imageE.get('gps_longitude'), imageE.get('gps_longitude_ref')),
            5.06255702, 6.13086962, 5.72626947, 2.12539276,
            2.03851195, 15.0338598, 42.3922098, 54.4202013,
            36.2102720, -77.0246007, -98.2080862
            ]
    })

    # affiche la carte
    st.map(data)
