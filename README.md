# NextBuy

> Projet académique — Epitech Bachelor 2028 · B-DAT-201

Dashboard analytique et prédictif pour l'analyse des comportements d'achat, basé sur le dataset Instacart.

## Fonctionnalités

- **Page 1 — Analyse** : KPIs globaux, top produits, commandes par jour de la semaine
- **Page 2 — Prédiction de rachat** : probabilité qu'un utilisateur rachète un produit donné, via Random Forest & Régression Logistique

## Stack

Python · Streamlit · Pandas · Scikit-learn · Plotly · Joblib

## Installation

```bash
pip install -r requirements.txt
```

Le dataset Instacart (`datasets/`) doit être présent à la racine (non versionné).

## Lancement

```bash
streamlit run main.py
```
