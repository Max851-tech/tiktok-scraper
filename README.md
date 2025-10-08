# TikTok Scraper - Conteneurisé

Application Python conteneurisée pour extraire les informations des vidéos d'un compte TikTok et les exporter en CSV.

## Fonctionnalités

- Extraction réelle des informations de vidéos TikTok avec yt-dlp :
  - URL de la vidéo
  - Description
  - Thumbnail
  - Nombre de vues
  - Nombre de likes
  - Nombre de commentaires
- Export automatique en fichier CSV
- Conteneurisation Docker complète
- Persistance des données hors du conteneur
- Gestion des erreurs robuste
- Logging détaillé

## Installation et Utilisation

### Prérequis

- Docker installé sur votre machine
- Docker Compose (optionnel mais recommandé)
- Connexion internet stable

### Méthode 1 : Avec Docker Compose (Recommandé)

\`\`\`bash
# Lancer le scraper
docker-compose up --build

# Les fichiers CSV seront créés dans le dossier ./data
\`\`\`

### Méthode 2 : Avec Docker uniquement

\`\`\`bash
# Construire l'image
docker build -t tiktok-scraper .

# Lancer le conteneur
docker run --shm-size=2gb -v $(pwd)/data:/app/data -e TIKTOK_USERNAME=hugodecrypte tiktok-scraper

# Sur Windows PowerShell, utilisez ${PWD} au lieu de $(pwd)
\`\`\`

### Méthode 3 : Exécution locale (sans Docker)

\`\`\`bash
# Installer les dépendances
pip install yt-dlp

# Lancer le scraper
python scraper.py
\`\`\`

## Configuration

### Variables d'environnement

- `TIKTOK_USERNAME` : Nom d'utilisateur TikTok à scraper (défaut: `hugodecrypte`)
- `MAX_VIDEOS` : Nombre maximum de vidéos à extraire (défaut: `10`)

Modifier dans `docker-compose.yml` :

\`\`\`yaml
environment:
  - TIKTOK_USERNAME=votre_username
  - MAX_VIDEOS=20
\`\`\`

## Structure du projet

\`\`\`
tiktok-scraper/
│
├── scraper.py              # Script Python principal avec yt-dlp
├── Dockerfile              # Configuration Docker
├── docker-compose.yml      # Orchestration Docker
├── README.md               # Documentation
├── .gitignore              # Fichiers à ignorer par Git
└── data/                   # Dossier de sortie CSV (créé automatiquement)
    └── *.csv               # Fichiers CSV générés
\`\`\`

## Format du fichier CSV

Le fichier CSV généré contient les colonnes suivantes :

| Colonne      | Description                    |
|--------------|--------------------------------|
| url          | URL de la vidéo TikTok        |
| description  | Description de la vidéo       |
| thumbnail    | URL de la miniature           |
| views        | Nombre de vues                |
| likes        | Nombre de likes               |
| comments     | Nombre de commentaires        |

Nom du fichier : `{username}_{timestamp}.csv`

Exemple : `hugodecrypte_20250108_143022.csv`

## Architecture technique

### Classe `TikTokScraper`

- **`__init__`** : Initialisation avec username et répertoire de sortie
- **`scrape_videos`** : Extraction des données vidéo avec yt-dlp
- **`export_to_csv`** : Export des données en CSV
- **`run`** : Orchestration complète du processus

### Technologie de scraping

Le scraper utilise **yt-dlp**, un outil professionnel pour extraire des métadonnées de plateformes vidéo :
- Extraction fiable sans détection de bot
- Contournement naturel des protections anti-scraping
- Support natif de TikTok
- Parsing automatique des statistiques
- Pas de CAPTCHA ou blocage

### Gestion des erreurs

- Logging détaillé de toutes les opérations
- Try-catch sur les opérations critiques
- Messages d'erreur explicites
- Codes de sortie appropriés
- Timeout de 5 minutes pour l'extraction

## Dépannage

### Le scraper ne trouve pas de vidéos

Vérifications :
- Le username TikTok est correct
- Le compte n'est pas privé
- Votre connexion internet fonctionne
- yt-dlp est à jour (peut nécessiter une mise à jour)

\`\`\`bash
# Mettre à jour yt-dlp
pip install --upgrade yt-dlp
\`\`\`

### Erreur de mémoire partagée

\`\`\`bash
# Augmenter la mémoire partagée
docker-compose down
# Modifier shm_size dans docker-compose.yml
docker-compose up --build
\`\`\`

### Le dossier data n'est pas créé

\`\`\`bash
mkdir data
chmod 755 data
\`\`\`

### Erreur de permissions Docker

\`\`\`bash
# Linux/Mac
sudo docker-compose up --build

# Ou ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER
\`\`\`

### Les logs ne s'affichent pas

Vérifiez que `PYTHONUNBUFFERED=1` est bien défini dans le Dockerfile.

## Notes importantes

### Considérations légales

Le scraping de TikTok peut violer les conditions d'utilisation de la plateforme. Cette application est fournie à des fins éducatives et de test technique. Utilisez-la de manière responsable et conformément aux lois applicables.

### Limitations

- TikTok peut limiter le taux de requêtes
- Certaines vidéos privées ne seront pas accessibles
- Le nombre de vidéos est limité par défaut à 10
- L'extraction peut prendre quelques minutes

### Améliorations possibles

- Ajouter un système de retry en cas d'échec
- Supporter la pagination pour plus de vidéos
- Ajouter l'export en JSON
- Implémenter un cache pour éviter les requêtes répétées
- Ajouter des filtres par date ou popularité

## Contact

Pour toute question ou amélioration, n'hésitez pas à ouvrir une issue sur le repository.

## Licence

Ce projet est fourni à des fins éducatives et de démonstration technique.
