# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:40:29 2023

@author: frup87122
"""

import streamlit as st
import pandas as pd
import altair as alt

# Charger les paramètres 
data_dir = "data"
# Ouvrir le fichier params.txt en mode lecture
with open(f"{data_dir}/Parameter_Datatype.txt", 'r') as file:
    # Lire toutes les lignes du fichier
    lines = file.readlines()

# Supprimer la première ligne d'en-tête
header = lines.pop(0)

# Recuperation des paramètres
l_params = [line.strip().split('\t')[0] for line in lines]
l_types = [line.strip().split('\t')[1] for line in lines]


file_param_path = 'data/Parameter_Datatype.txt'
data = pd.read_csv(file_path, index_col="Unnamed: 0")
data["indice"] =data.index


# Convertir les colonnes spécifiées en entiers
data = data.replace(',', '.', regex=True)
data = data.rename(columns=lambda x: x.split(' [')[0])

# Sidebar
st.sidebar.title("Paramètres du graphe")
feature_col = st.sidebar.selectbox("Abscisse :", data.columns)
target_col = st.sidebar.selectbox("Ordonnée :", data.columns)
color_col = st.sidebar.selectbox("Couleur :", data.columns)

# Personnaliser les bulles d'informations
hover_cols = st.sidebar.multiselect("Choisir les colonnes pour les bulles d'infos :", data.columns)
hover_cols = [feature_col, target_col, color_col] + hover_cols  

# Afficher le DataFrame dans la page centrale
st.title("DataFrame")
st.write(data)

# Créer un scatter plot avec Altair
st.title("Representation des jeux de train et de test")

# Votre code Altair pour le graphique de dispersion
scatter_chart = alt.Chart(data).mark_circle().encode(
    x=alt.X(feature_col),  # Fixer l'origine en bas à gauche
    y=alt.Y(target_col),  # Fixer l'origine en bas à gauche
    color=color_col,
    tooltip=list(hover_cols)
).interactive()


# Afficher le plot dans la page centrale
selected_point = st.altair_chart(scatter_chart, use_container_width=True)
