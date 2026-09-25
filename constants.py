#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : constants.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-09-25
Modifié le    : 2026-09-25
Version       : 0.7.0
Copyright     : Pierre Théberge

Description
-----------
Délais d'attente et pauses utilisés avec Selenium, en secondes.

Les ATTENTE_* sont des délais maximaux (WebDriverWait) : l'attente se termine
dès que la condition est remplie. Les PAUSE_* sont des pauses fixes
(time.sleep) : elles s'écoulent en entier à chaque passage.

Modifications
-------------
0.7.0 - 2026-09-25   ES-29 : Version initiale : centralisation des délais et pauses.

Paramètres
----------
N/A (module importé par l'application).

Exemple
-------
>>> from constants import ATTENTE_ELEMENT
>>> WebDriverWait(driver, ATTENTE_ELEMENT).until(...)
"""

# --- Délais maximaux (WebDriverWait) ---

# Élément facultatif : son absence est un cas normal (bouton « Pas maintenant »,
# champ déjà affiché, premier sélecteur d'une liste de replis).
ATTENTE_OPTIONNELLE = 5

# Vérification qu'un rapport est bien l'onglet actif.
ATTENTE_ETAT_RAPPORT = 8

# Élément attendu sur une page déjà chargée.
ATTENTE_ELEMENT = 10

# Sélecteur de repli, tenté après l'échec du sélecteur principal.
ATTENTE_REPLI = 20

# Élément qui suit une navigation ou un rechargement partiel.
ATTENTE_PAGE = 30

# Page complète ou élément long à apparaître (boutons de téléchargement,
# panneau des dates).
ATTENTE_CHARGEMENT = 60

# Fin d'un téléchargement ou libération d'un fichier verrouillé (WinError 32).
ATTENTE_TELECHARGEMENT = 120

# Vérification humaine Cloudflare, complétée à la main par l'utilisateur.
ATTENTE_CLOUDFLARE = 600

# --- Pauses fixes (time.sleep) ---

# Entre deux gestes de saisie dans un même champ.
PAUSE_SAISIE = 0.5

# Après un clic qui ne déclenche qu'un changement local.
PAUSE_COURTE = 1

# Après un clic qui redessine une partie de la page.
PAUSE_UI = 2

# Rendu des graphiques d'un sous-rapport Comparer.
PAUSE_RENDU_GRAPHIQUE = 3

# Après la déconnexion, avant de fermer le navigateur.
PAUSE_APRES_DECONNEXION = 3

# Après une action qui charge une nouvelle vue (connexion, génération du PDF).
PAUSE_ACTION = 5

# Après la fermeture de la fenêtre de téléchargement, le temps que le fichier
# soit écrit en entier.
PAUSE_FINALISATION_TELECHARGEMENT = 10

# Silence après le bouton Home User, pour ne pas relancer la vérification
# Cloudflare par des interactions trop rapprochées.
PAUSE_SILENCE_CLOUDFLARE = 45

# Après le dernier rapport, avant la déconnexion.
PAUSE_AVANT_DECONNEXION = 60
