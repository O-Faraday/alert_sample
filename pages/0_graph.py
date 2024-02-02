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
    dates = pd.date_range(end=pd.Timestamp.now(), periods=10, freq='S')
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

# Créer un placeholder pour l'histogramme
placeholder = st.empty()

# Boucle pour mettre à jour le DataFrame et l'affichage
while True:
    # Ajouter un nouvel enregistrement au DataFrame
    df = add_new_record(df)
    
    # Sélectionner la dernière ligne du DataFrame pour l'histogramme
    last_row = df.iloc[-1]
    
    # Créer l'histogramme avec Matplotlib
    fig, ax = plt.subplots()
    ax.hist(last_row, bins=20, color='blue', alpha=0.7)
    ax.set_title("Distribution des valeurs pour le dernier enregistrement")
    ax.set_xlabel("Valeur")
    ax.set_ylabel("Fréquence")
    
    # Afficher l'histogramme dans Streamlit
    placeholder.pyplot(fig)
    
    # Attendre une seconde avant la prochaine mise à jour
    time.sleep(5)
    
    # Effacer les anciens graphiques pour ne pas surcharger la page
    st.empty()
