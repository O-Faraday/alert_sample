# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:40:29 2023

@author: frup87122
"""

import streamlit as st
import pandas as pd
import altair as alt

# 1- Charger les paramètres 
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

# On garde que les floats pour commencer
keep_types = ['float']
l_keep_params = [p  for p, t in zip(l_params, l_types) if t in keep_types]

# 
# 2- Selection des paramètres que l'on souhaite afficher
selected_params = st.sidebar.multiselect("Choisir les paramètres à affichers :", l_keep_params)

# 3- Affichage des paramètres au cours du temps
for param in selected_params :
    file_path = 'f"{data_dir}/csv/{param}.csv.zip'
    data = pd.read_csv(file_path, index_col="Unnamed: 0")
    data["indice"] =data.index
    # Afficher le DataFrame dans la page centrale
    st.title("DataFrame")
    st.write(data)



