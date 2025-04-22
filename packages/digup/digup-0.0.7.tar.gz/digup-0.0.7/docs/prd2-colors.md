
Détecter le mode dispo : 
- 256 ?
- True color ? 

Dans PyCharm : True Color
Dans Terminal : 256 (déjà largement assez de couleurs ?)

Utiliser le mode le plus riche par défaut. 

Permettre de sélectionner de façon explicite (via pyproject)

Modes : 
- palette
  - dynamique (hsv de la longueur du nombre d'identifiants)
  - statique : distinct 255^3/6^3, lerp on 255^3/6^3 (+ tail) (on peut faire des palettes exponentielles ->> juste donner le niveau ?) (2^3-2, 3^3-2, 4^3-2, ...)
- filtres (peuvent être combinés)
  - seuil d'occurrences (ex : ne colorier que si +1 occurrence)
  - seuil de span (ex : ne colorier que si span > 1)
  - plafond de span (ex : ne colorier que si span < 10)
  - params only
  - words only
  - exclude some words
- limiter (mutuellement exclusifs)
  - --first n (ne colorier que les n premiers identifiants)
  - --last n (ne colorier que les n derniers identifiants)
  - --most n (ne colorier que les n identifiants les + récurrents)
  - --least n (ne colorier que les n identifiants les - récurrents)


Décision : 
- implémenter uniquement 256 pour commencer.
- partir sur la palette statique HSV
- garder les palettes dynamiques RGB pour + tard