@echo off
REM Exemple d'utilisation du compresseur d'images WebP
REM Ce fichier montre quelques commandes courantes

echo Compresseur d'images WebP - Exemples d'utilisation
echo ===================================================

REM Installation des dépendances (une seule fois)
echo 1. Installer les dependances Python:
echo    pip install -r requirements.txt
echo.

REM Compression basique
echo 2. Compression basique d'un dossier:
echo    python compress_images.py ./mes_photos
echo.

REM Compression avec options
echo 3. Compression avec qualite personnalisee:
echo    python compress_images.py ./images --quality 75
echo.

REM Compression recursive avec sortie personnalisee
echo 4. Compression recursive avec dossier de sortie:
echo    python compress_images.py ./collection --recursive --output ./webp_optimise
echo.

REM Compression haute qualite
echo 5. Compression haute qualite:
echo    python compress_images.py ./portfolio --quality 95 --method 6
echo.

pause