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
def create_initial_df():
    # Créer une colonne de dates
    dates = pd.date_range(end=pd.Timestamp.now(), periods=10, freq='2s')
    # Générer des valeurs aléatoires entre 0 et 255 pour les 256 colonnes
    data = np.random.randint(0, 256, size=(10, 256))
    df = pd.DataFrame(data, index=dates)
    return df
    
# Fonction pour ajouter un nouvel enregistrement au DataFrame
def add_new_record(df):
    # Ajouter un nouvel enregistrement avec la date actuelle
    new_row = pd.DataFrame(np.random.randint(0, 256, size=(1, 256)), index=[pd.Timestamp.now()])
    df = pd.concat([df, new_row])
    return df


# Initialiser le DataFrame
df = create_initial_df()

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
sliding_window = st.sidebar.slider("Sélectionnez la durée de la fenêtre glissante (en enregistrements) : ", 1, 20, 10)  # Défaut à 5
alert_threshold = st.sidebar.slider("Sélectionnez le seuil d'alerte : ", 0, 50*sliding_window, 20*sliding_window)  


# Boucle pour mettre à jour le DataFrame et l'affichage
while True:
    # Fermer toutes les figures ouvertes avant de créer une nouvelle figure
    plt.close('all')  # Ajoutez cette ligne pour s'assurer que toutes les figures précédentes sont fermées

    # Ajouter un nouvel enregistrement au DataFrame
    df = add_new_record(df)

    # Calculer l'alerte sur la fenêtre glissante
    windowed_data = df.iloc[-sliding_window:]
    count_above_threshold = (windowed_data > seuil).sum(axis=1)
    alert_indicator = 1 if any(count_above_threshold > alert_threshold) else 0
    new_alert = pd.DataFrame({'Date': [pd.Timestamp.now()], 'Alert': [alert_indicator]})
    alert_df = pd.concat([alert_df, new_alert])
    
    # Sélectionner la dernière ligne du DataFrame pour l'histogramme
    last_row = df.iloc[-1].values

    
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
    alert_placeholder.pyplot(fig)
    
    # Attendre une seconde avant la prochaine mise à jour
    time.sleep(2)
    
    # Nettoyage pour éviter la surcharge de la page
    placeholder.empty()
    alert_placeholder.empty()
