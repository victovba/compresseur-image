# Compresseur d'Images WebP

Outil simple de compression d'images en masse pour convertir des fichiers JPEG/PNG en WebP léger.

## Installation

1. Installer les dépendances Python :
```bash
pip install -r requirements.txt
```

## Utilisation

### Commande de base
```bash
python compress_images.py /chemin/vers/votre/dossier
```

### Options disponibles

| Option | Description | Valeur par défaut |
|--------|-------------|-------------------|
| `--quality`, `-q` | Niveau de qualité WebP (0-100) | 80 |
| `--recursive`, `-r` | Parcourir les sous-répertoires | Non |
| `--output`, `-o` | Répertoire de sortie spécifique | Même dossier que les sources |
| `--method`, `-m` | Méthode de compression (0-6) | 4 |
| `--no-metadata` | Ne pas préserver les métadonnées EXIF/ICC | Non |

### Exemples

1. **Compression basique** (qualité 80, mêmes dossiers) :
```bash
python compress_images.py ./mes_photos
```

2. **Compression avec qualité personnalisée** :
```bash
python compress_images.py ./images --quality 75
```

3. **Compression récursive avec sortie dans un dossier dédié** :
```bash
python compress_images.py ./collection --recursive --output ./webp_optimise
```

4. **Haute qualité pour photos professionnelles** :
```bash
python compress_images.py ./portfolio --quality 95
```

## Formats supportés

- **Entrée** : JPEG, PNG, BMP, TIFF
- **Sortie** : WebP

## Caractéristiques

- ✅ Compression en masse automatique
- ✅ Préservation des métadonnées EXIF/ICC
- ✅ Support de la transparence PNG → WebP
- ✅ Conservation des fichiers originaux
- ✅ Interface ligne de commande simple
- ✅ Affichage de la progression et réduction de taille

## Paramètres de compression recommandés

| Usage | Qualité | Méthode |
|-------|---------|---------|
| Photos pour web | 80 | 4 |
| Haute qualité (impression) | 95 | 6 |
| Compression maximale | 60 | 6 |
| Icônes/logos avec transparence | 90 | 4 |

## Notes techniques

- Le script utilise la bibliothèque Pillow (PIL) pour la conversion
- La compression WebP lossy est utilisée par défaut
- Les images avec transparence (PNG) sont automatiquement détectées et traitées
- Les métadonnées EXIF et ICC sont préservées pour maintenir la fidélité colorimétrique

## Dépannage

**Erreur : "Le support WebP n'est pas disponible"**
- Vérifiez que Pillow est correctement installé : `pip install --upgrade Pillow`

**Aucune image trouvée**
- Vérifiez le chemin du répertoire
- Assurez-vous que le dossier contient des fichiers avec les extensions : .jpg, .jpeg, .png, .bmp, .tiff

**Mauvaise qualité de sortie**
- Augmentez la qualité (--quality 90-95)
- Utilisez une méthode de compression plus élevée (--method 6)

## Licence

Outil open source généré par opencode.