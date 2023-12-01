# Sprint_Booster2_Waykonect
Algos Hierarchie - Repartition

Fichiers d'entrée requis : 0_Users_list.csv ; 3_EVSE_list.csv

Algos Python à lancer dans l'ordre : 2_Waiting_lists.py ; 4_Planification_week_ahead.py
  - Chemins des fichiers entrée/intermédiaire/sortie en dur dans les algos mais en chemins relatifs
  - Donc package téléchargé dans un dossier -> scripts à lancer dans ce dossier
  - 
Fichier de sortie : 5_Planning_week_ahead.csv
  - Algo lancé jour J : planning de J+1 à J+7
  - 1 ligne par créneau de réservation
  - 1 ligne comprend : 1 EVSE, 1 utilisateur, 1 date de début de session (8h le matin et 13h l'après-midi), 1 date de fin de session (13h le matin et 19h le soir), la confirmation utilisateur validée par défaut
