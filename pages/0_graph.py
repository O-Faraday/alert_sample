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

# Créer un placeholder pour l'histogramme
placeholder = st.empty()

# Créer un curseur dans la sidebar pour sélectionner une valeur entre 0 et 255
seuil = st.sidebar.slider("Sélectionnez le seuil de température", 0, 255, 200)  # Défaut à 128

# Boucle pour mettre à jour le DataFrame et l'affichage
while True:
    # Fermer toutes les figures ouvertes avant de créer une nouvelle figure
    plt.close('all')  # Ajoutez cette ligne pour s'assurer que toutes les figures précédentes sont fermées

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
    
    # Ajouter une ligne verticale en pointillés à la valeur 128
    ax.axvline(x=seuil, color='red', linestyle='--', linewidth=2, label='Valeur fixe 128')

    # Ajouter une légende pour expliciter ce que représente la ligne
    ax.legend()
    
    # Afficher l'histogramme dans Streamlit
    placeholder.pyplot(fig)

    #Décompte des valeurs au dela du seuil
    count_above = np.sum(last_row > seuil)
    
    # Attendre une seconde avant la prochaine mise à jour
    time.sleep(2)
    
    # Effacer les anciens graphiques pour ne pas surcharger la page
    st.empty()
