# Classification des paragraphes des textes du JO

Les données utilisées par cet outil sont les données du JORF organisées dans un CSV avec 6 colonnes:

- Identifiant du texte: `JORFTEXTxxxx` (`str`)
- Identifiant de ressource enfant: `JORFVERSxxxx` pour une version de texte ou `JORFARTIxxx` pour un article ou vide (`str`)
- Type de paragraphe: 1=ALINEA 2=TABLE 3=RAW (`int`)
- Numéro de l'article (`str` ou vide)
- Rang du paragraphe, démarrant à 1 (`int`)
- Contenu (`str`)

## Classification des paragraphes modificateurs

Génération d'un CSV avec les paragraphes classifiés selon leur catégorie de modification induite:

```bash
dqclassify_csv jorf.csv
```

Voir les [catégories de modification](dqclassify/categories.py).

Le CSV obtenu a une colonne supplémentaire par rapport au CSV source juste avant le contenu:

- Identifiant du texte: `JORFTEXTxxxx` (`str`)
- Identifiant de ressource enfant: `JORFVERSxxxx` pour une version de texte ou `JORFARTIxxx` pour un article ou vide (`str`)
- Type de paragraphe: 1=ALINEA 2=TABLE 3=RAW (`int`)
- Numéro de l'article (`str` ou vide)
- Rang du paragraphe, démarrant à 1 (`int`)
- **Classification du paragraphe modificateur (`categories.ModifierCategory.value: int` ou vide)**
- Contenu (`str`)

