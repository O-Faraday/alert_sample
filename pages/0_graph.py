# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:40:29 2023

@author: frup87122
"""
import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Fonction pour créer un DataFrame initial
def create_initial_df(time_step=1):
    # Créer une colonne de dates
    dates = pd.date_range(end=pd.Timestamp.now(), periods=10, freq=f'{time_step}s')
    # Générer des valeurs aléatoires entre 0 et 255 pour les 256 colonnes
    data = np.vstack([create_array_and_add_gaussian().reshape(1,256) for i in range(10)])
    df = pd.DataFrame(data, index=dates)
    return df
    
# Fonction pour ajouter un nouvel enregistrement au DataFrame
def add_new_record(df):
    # Ajouter un nouvel enregistrement avec la date actuelle
    new_row = pd.DataFrame(create_array_and_add_gaussian().reshape(1,256), index=[pd.Timestamp.now()])
    df = pd.concat([df, new_row])
    return df

# Creer le rectangle dans l'image
def create_rectangle_array():
    # Créer un tableau de 16x16 avec des valeurs constantes à 55
    array = np.full((16, 16), 55, dtype=int)
    
    # Choisir un centre au hasard dans le tableau
    center = np.random.randint(0, 16, size=2)
    
    # Choisir des dimensions aléatoires pour le rectangle avec largeur < 8 et longueur < 8
    width = np.random.randint(1, 8)
    length = np.random.randint(1, 8)
    
    # Calculer les coordonnées du coin supérieur gauche du rectangle
    top_left = center - np.array([length//2, width//2])
    
    # Ajuster pour s'assurer que le rectangle reste dans les limites du tableau
    top_left = np.clip(top_left, 0, 16 - np.array([length, width]))
    
    # Calculer les coordonnées du coin inférieur droit du rectangle
    bottom_right = top_left + np.array([length, width])
    
    # Délimiter le rectangle dans le tableau (ici, vous pouvez choisir de modifier les valeurs ou de les laisser identiques)
    # array[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]] = # Valeur à définir si nécessaire
    
    return center, length, width
    
# Creation de la gaussienne superposée au tableau
def add_gaussian_to_array(center, length, width, array):
    height = np.random.randint(100, 201)  # Hauteur aléatoire entre 100 et 200

    # Créer des grilles de coordonnées pour le tableau
    x = np.arange(0, array.shape[0])
    y = np.arange(0, array.shape[1])
    x_grid, y_grid = np.meshgrid(x, y)

    # Calculer la gaussienne
    sigma_x = length 
    sigma_y = width 
    gauss = height * np.exp(-(((x_grid - center[0])**2 / (2 * sigma_x**2)) + ((y_grid - center[1])**2 / (2 * sigma_y**2))))

    # Convertir les valeurs de la gaussienne en entiers
    gauss_int = np.round(gauss).astype(int)

    # Ajouter la gaussienne au tableau existant
    array += gauss_int
    return array

# Fonction pour créer un tableau et ajouter une gaussienne
def create_array_and_add_gaussian():
    array = np.full((16, 16), 55, dtype=int)  # Tableau initial
    center, length, width = create_rectangle_array()  # Obtenir centre, longueur, et largeur (définir cette fonction séparément)
    array_with_gaussian = add_gaussian_to_array(center, length, width, array)  # Ajouter la gaussienne
    return array_with_gaussian


# Initialiser le DataFrame
time_intervall=2
df = create_initial_df(time_intervall)

# Titre de l'application Streamlit
st.title("Visualisation en temps réel des données")

# DataFrame pour stocker les indicateurs d'alerte
alert_df = pd.DataFrame(columns=['Date', 'Alert'])

# Créer un placeholder pour l'histogramme
placeholder = st.empty()

# Créer un placeholder pour le graphique d'alerte
alert_placeholder = st.empty()

# Paramètres de la sidebar
seuil = st.sidebar.slider("Sélectionnez le seuil de température", 0, 255, 200)  # Défaut à 200
sliding_window = st.sidebar.slider("Sélectionnez la durée de la fenêtre glissante (en enregistrements) : ", 0, 10*time_intervall, 5*time_intervall, step=time_intervall)  # Défaut à 5
alert_threshold = st.sidebar.slider("Sélectionnez le seuil d'alerte : ", 0, 50*sliding_window, 20*sliding_window)  

compteur = 0
# Boucle pour mettre à jour le DataFrame et l'affichage
while True:
    # Fermer toutes les figures ouvertes avant de créer une nouvelle figure
    plt.close('all')  # Ajoutez cette ligne pour s'assurer que toutes les figures précédentes sont fermées
    st.write(f"compteur : {compteur}")
    # Ajouter un nouvel enregistrement au DataFrame
    df = add_new_record(df)

    # Calculer l'alerte sur la fenêtre glissante
    windowed_data = df.iloc[-sliding_window//time_intervall:]
    count_above_threshold = (windowed_data.values > seuil).sum()
    st.write("count_above_threshold")
    st.write(count_above_threshold)
    alert_indicator = 1 if count_above_threshold > alert_threshold else 0
    new_alert = pd.DataFrame({'Date': [pd.Timestamp.now()], 'Alert': [alert_indicator]})
    st.write("new_alert")
    st.write(new_alert)
    if alert_df.empty:
       alert_df = new_alert.copy()
    else :
       alert_df = pd.concat([alert_df, new_alert])
    st.write("alert_df")
    st.write(alert_df)
    
    # Sélectionner la dernière ligne du DataFrame pour l'histogramme
    last_row = df.iloc[-1].values
    count_threshold = (last_row > seuil).sum()
    st.write("count_threshold")
    st.write(count_threshold)
    
    # Préparer les données pour l'image
    data_for_image = last_row.reshape((16, 16))
    image = np.zeros((16, 16, 3), dtype=np.uint8)  # Créer un tableau vide pour l'image RGB
    image[:, :, 0] = data_for_image  # Canal rouge
    image[:, :, 2] = 255 - data_for_image  # Canal bleu
    # Le canal vert reste à 0

    # Créer l'histogramme avec Matplotlib
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].hist(last_row, bins=20, color='blue', alpha=0.7)
    axs[0].set_title("Distribution des valeurs pour le dernier enregistrement")
    axs[0].set_xlabel("Valeur")
    axs[0].set_ylabel("Fréquence")
    axs[0].axvline(x=seuil, color='red', linestyle='--', linewidth=2, label=f'Valeur sélectionnée {seuil}')
    axs[0].legend()

    # Afficher l'image à côté de l'histogramme
    axs[1].imshow(image)
    axs[1].set_title("Représentation en image")
    axs[1].axis('off')  # Désactiver les axes pour l'image
    
    # Afficher l'histogramme dans Streamlit
    placeholder.pyplot(fig)

    # Affichage du graphique d'alerte
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(alert_df['Date'], alert_df['Alert'], marker='o', linestyle='-', color='red')
    ax.set_title("Indicateur d'alerte au fil du temps")
    ax.set_xlabel("Temps")
    ax.set_ylabel("Alerte")
    ax.set_ylim(-0.1, 1.1)

    # Pour améliorer la lisibilité des dates sur l'axe des x
    fig.autofmt_xdate()

    # Afficher le graphique dans le placeholder Streamlit
    alert_placeholder.pyplot(fig)

    # Attendre une seconde avant la prochaine mise à jour
    time.sleep(time_intervall)
    
    # Nettoyage pour éviter la surcharge de la page
    #placeholder.empty()
    #alert_placeholder.empty()
