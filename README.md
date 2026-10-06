# Bruno Brain Clinic

[English](README.en.md) · [Español](README.es.md)

Un vérificateur **local et en lecture seule** pour les exports Markdown de mémoire d'agents, dont [Bruno Brain](https://get-bruno.com/fr/tech). Il signale les pages sans source, les dates de péremption dépassées, quelques motifs de secrets et les valeurs contradictoires qui portent explicitement le même fact_key. Le rapport ne contient pas les valeurs des faits ni les secrets détectés.

Le dossier skills/brain-clinic contient une compétence d'agent réutilisable pour lancer cet examen localement.

## Essayer

    python3 -m pip install -r requirements.txt
    python3 brain_clinic.py CHEMIN_EXPORT --lang fr
    python3 -m unittest discover -s tests -v

Les métadonnées, lorsqu'elles existent, sont du YAML entre deux lignes --- en tête du Markdown. Les champs compris par cette version sont sources ou source, stale_after au format YYYY-MM-DD, et les champs optionnels fact_key et fact_value pour comparer des faits. Un lien présent dans le corps peut aussi servir de source. Le programme lit tous les fichiers .md du dossier et produit du JSON. Codes de sortie : 0 aucun signalement, 2 vérification nécessaire, 1 entrée invalide. Les messages existent en français, anglais et espagnol.

Bruno annonce l'export de son cerveau en Markdown ou OKF. Ce dépôt travaille sur les fichiers Markdown exportés ; il ne se connecte pas à Bruno et ne valide pas l'ensemble de la spécification OKF. Il ne détecte que les contradictions explicitement identifiées par fact_key, pas les divergences sémantiques. Vérifiez les signalements avant toute correction.

Licence MIT.
