#!/bin/bash
# Exemple d'utilisation du compresseur d'images WebP
# Ce fichier montre quelques commandes courantes

echo "Compresseur d'images WebP - Exemples d'utilisation"
echo "==================================================="

# Installation des dépendances (une seule fois)
echo "1. Installer les dépendances Python:"
echo "   pip install -r requirements.txt"
echo ""

# Compression basique
echo "2. Compression basique d'un dossier:"
echo "   python compress_images.py ./mes_photos"
echo ""

# Compression avec options
echo "3. Compression avec qualité personnalisée:"
echo "   python compress_images.py ./images --quality 75"
echo ""

# Compression recursive avec sortie personnalisée
echo "4. Compression récursive avec dossier de sortie:"
echo "   python compress_images.py ./collection --recursive --output ./webp_optimise"
echo ""

# Compression haute qualité
echo "5. Compression haute qualité:"
echo "   python compress_images.py ./portfolio --quality 95 --method 6"
echo ""

# Pour rendre ce script exécutable
chmod +x "$0" 2>/dev/null || true