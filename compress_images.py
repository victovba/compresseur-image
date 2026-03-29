#!/usr/bin/env python3
"""
Outil de compression d'images en masse JPEG/PNG → WebP
Auteur: Généré par opencode
Date: 2026-03-29
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any
from PIL import Image, features


class WebPCompressor:
    """Classe principale pour la conversion d'images en WebP."""
    
    def __init__(self, quality: int = 80, method: int = 4, 
                 preserve_metadata: bool = True, exact: bool = True):
        """
        Initialise le compresseur WebP.
        
        Args:
            quality: Niveau de qualité WebP (0-100)
            method: Méthode de compression (0-6, 4 par défaut)
            preserve_metadata: Préserver les métadonnées EXIF/ICC
            exact: Préserver les valeurs RGB dans les pixels transparents
        """
        self.quality = max(0, min(100, quality))
        self.method = max(0, min(6, method))
        self.preserve_metadata = preserve_metadata
        self.exact = exact
        
        # Vérifier le support WebP
        if not features.check('webp'):
            raise ImportError("Le support WebP n'est pas disponible. Vérifiez que Pillow est correctement installé.")
    
    def compress_image(self, input_path: Path, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Compresse une image en WebP.
        
        Args:
            input_path: Chemin de l'image source
            output_path: Chemin de sortie (optionnel)
            
        Returns:
            Dictionnaire avec les résultats de la conversion
        """
        if output_path is None:
            output_path = input_path.with_suffix('.webp')
        
        try:
            with Image.open(input_path) as img:
                # Sauvegarder les métadonnées originales
                metadata = {}
                if self.preserve_metadata:
                    for key in ['icc_profile', 'exif', 'xmp']:
                        if key in img.info:
                            metadata[key] = img.info[key]
                
                # Gérer la transparence
                has_transparency = img.mode in ('RGBA', 'LA') or (
                    img.mode == 'P' and 'transparency' in img.info
                )
                
                # Convertir en RGBA si nécessaire pour la transparence
                if has_transparency:
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    save_options = {
                        'format': 'WEBP',
                        'quality': self.quality,
                        'method': self.method,
                        'lossless': False,
                        'exact': self.exact,
                        'alpha_quality': 100
                    }
                else:
                    # Conversion sans transparence
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    save_options = {
                        'format': 'WEBP',
                        'quality': self.quality,
                        'method': self.method,
                        'lossless': False
                    }
                
                # Ajouter les métadonnées sauvegardées
                save_options.update(metadata)
                
                # Sauvegarder l'image
                img.save(output_path, **save_options)
                
                # Calculer les statistiques
                original_size = input_path.stat().st_size
                compressed_size = output_path.stat().st_size
                reduction_percent = (1 - compressed_size / original_size) * 100
                
                return {
                    'success': True,
                    'input_path': str(input_path),
                    'output_path': str(output_path),
                    'original_size': original_size,
                    'compressed_size': compressed_size,
                    'reduction_percent': reduction_percent,
                    'has_transparency': has_transparency
                }
                
        except Exception as e:
            return {
                'success': False,
                'input_path': str(input_path),
                'error': str(e)
            }
    
    def batch_compress(self, input_dir: Path, output_dir: Optional[Path] = None, 
                       recursive: bool = False) -> List[Dict[str, Any]]:
        """
        Compresse toutes les images d'un répertoire.
        
        Args:
            input_dir: Répertoire source
            output_dir: Répertoire de sortie (optionnel)
            recursive: Parcourir les sous-répertoires
            
        Returns:
            Liste des résultats de conversion
        """
        # Créer le répertoire de sortie si nécessaire
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extensions d'images supportées
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        # Trouver toutes les images
        images = []
        if recursive:
            for ext in image_extensions:
                images.extend(input_dir.rglob(f'*{ext}'))
                images.extend(input_dir.rglob(f'*{ext.upper()}'))
        else:
            for ext in image_extensions:
                images.extend(input_dir.glob(f'*{ext}'))
                images.extend(input_dir.glob(f'*{ext.upper()}'))
        
        # Supprimer les doublons et trier
        images = sorted(list(set(images)))
        
        if not images:
            print(f"Aucune image trouvée dans {input_dir}")
            return []
        
        print(f"Trouvé {len(images)} image(s) à compresser")
        print("-" * 50)
        
        results = []
        for img_path in images:
            # Déterminer le chemin de sortie
            if output_dir:
                rel_path = img_path.relative_to(input_dir)
                output_path = output_dir / rel_path.with_suffix('.webp')
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = img_path.with_suffix('.webp')
            
            # Compresser l'image
            result = self.compress_image(img_path, output_path)
            results.append(result)
            
            # Afficher le résultat
            if result['success']:
                reduction = result['reduction_percent']
                size_info = f"{result['original_size'] // 1024}KB -> {result['compressed_size'] // 1024}KB"
                print(f"[OK] {img_path.name:<28} | {reduction:>5.1f}% | {size_info}")
            else:
                print(f"[ER] {img_path.name:<28} | ERREUR: {result['error']}")
        
        return results


def format_size(size_bytes: int) -> str:
    """Formate une taille en bytes en unité lisible."""
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def main():
    """Fonction principale de l'interface en ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Compresse des images JPEG/PNG en WebP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python compress_images.py ./photos
  python compress_images.py ./images --quality 75 --recursive
  python compress_images.py ./input --output ./webp --quality 90
        """
    )
    
    parser.add_argument(
        "input_dir",
        type=str,
        help="Répertoire contenant les images à compresser"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Répertoire de sortie (par défaut: même répertoire que les sources)"
    )
    
    parser.add_argument(
        "--quality", "-q",
        type=int,
        default=80,
        help="Niveau de qualité WebP (0-100, défaut: 80)"
    )
    
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Parcourir les sous-répertoires"
    )
    
    parser.add_argument(
        "--method", "-m",
        type=int,
        default=4,
        help="Méthode de compression (0-6, défaut: 4)"
    )
    
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Ne pas préserver les métadonnées EXIF/ICC"
    )
    
    args = parser.parse_args()
    
    # Valider le répertoire d'entrée
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"Erreur: Le répertoire '{args.input_dir}' n'existe pas.")
        sys.exit(1)
    
    if not input_dir.is_dir():
        print(f"Erreur: '{args.input_dir}' n'est pas un répertoire.")
        sys.exit(1)
    
    # Valider la qualité
    if not 0 <= args.quality <= 100:
        print(f"Erreur: La qualité doit être entre 0 et 100 (reçu: {args.quality})")
        sys.exit(1)
    
    # Valider la méthode
    if not 0 <= args.method <= 6:
        print(f"Erreur: La méthode doit être entre 0 et 6 (reçu: {args.method})")
        sys.exit(1)
    
    # Créer le compresseur
    try:
        compressor = WebPCompressor(
            quality=args.quality,
            method=args.method,
            preserve_metadata=not args.no_metadata
        )
    except ImportError as e:
        print(f"Erreur: {e}")
        sys.exit(1)
    
    # Déterminer le répertoire de sortie
    output_dir = Path(args.output) if args.output else None
    
    print(f"Compression WebP - Qualité: {args.quality}, Méthode: {args.method}")
    print(f"Source: {input_dir}")
    if output_dir:
        print(f"Destination: {output_dir}")
    print(f"Récursif: {'Oui' if args.recursive else 'Non'}")
    print()
    
    # Lancer la compression par lots
    results = compressor.batch_compress(input_dir, output_dir, args.recursive)
    
    # Afficher le résumé
    if results:
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        total_original = sum(r['original_size'] for r in successful)
        total_compressed = sum(r['compressed_size'] for r in successful)
        total_reduction = (1 - total_compressed / total_original) * 100 if total_original > 0 else 0
        
        print()
        print("=" * 50)
        print("RÉSUMÉ")
        print("=" * 50)
        print(f"Images traitées: {len(results)}")
        print(f"Réussies: {len(successful)}")
        print(f"Échouées: {len(failed)}")
        
        if successful:
            print(f"Taille originale totale: {format_size(total_original)}")
            print(f"Taille compressée totale: {format_size(total_compressed)}")
            print(f"Réduction totale: {total_reduction:.1f}%")
        
        if failed:
            print("\nErreurs:")
            for r in failed:
                print(f"  - {Path(r['input_path']).name}: {r['error']}")
        
        print()
        print(f"Les fichiers WebP {'ont été créés dans le répertoire de sortie' if output_dir else 'ont été créés à côté des fichiers originaux'}")
    
    sys.exit(0 if not any(not r['success'] for r in results) else 1)


if __name__ == "__main__":
    main()