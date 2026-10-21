#!/usr/bin/env python3
"""
Optimiza las fotos de la audioguía: las reduce y las pasa a WebP.

Uso:
    python3 tools/optimizar-fotos.py  carpeta_con_fotos_originales

Deja los WebP en img/fotos/ con el mismo nombre. No toca los originales.

Qué tamaños usa y por qué:
  - *_hero.*  -> 1200 px de ancho  (la imagen grande de cada exhibición)
  - el resto  ->  800 px de ancho  (las fotos de "cómo hacerla bien")

Pon el sufijo _hero en el nombre si una foto es la principal de la ficha.
Ejemplo:  52_paradox-challenge_hero.jpg  ->  img/fotos/52_paradox-challenge_hero.webp
"""

import sys, os
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Falta Pillow.  Instálalo con:  pip install Pillow")

CALIDAD = 80          # 80 da buena imagen; baja a 72 si quieres pesar menos
ANCHO_HERO = 1200
ANCHO_PASO = 800
ENTRADAS = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".tif", ".tiff"}

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    origen = Path(sys.argv[1]).expanduser()
    if not origen.is_dir():
        sys.exit(f"No existe la carpeta: {origen}")

    destino = Path(__file__).resolve().parent.parent / "img" / "fotos"
    destino.mkdir(parents=True, exist_ok=True)

    fotos = sorted(p for p in origen.iterdir()
                   if p.is_file() and p.suffix.lower() in ENTRADAS)
    if not fotos:
        sys.exit(f"No he encontrado fotos en {origen}")

    total_antes = total_despues = 0
    for p in fotos:
        try:
            im = Image.open(p)
        except Exception as e:
            print(f"  !! {p.name}: no se puede abrir ({e})")
            continue

        im = ImageOps.exif_transpose(im).convert("RGB")   # respeta la rotación
        ancho = ANCHO_HERO if "_hero" in p.stem.lower() else ANCHO_PASO
        if im.width > ancho:
            im.thumbnail((ancho, ancho * 3), Image.LANCZOS)

        salida = destino / (p.stem + ".webp")
        im.save(salida, "WEBP", quality=CALIDAD, method=6)

        antes, despues = p.stat().st_size, salida.stat().st_size
        total_antes += antes; total_despues += despues
        print(f"  {p.name:42s} {antes/1024:7.0f} KB -> {despues/1024:6.0f} KB "
              f"({im.width}x{im.height})")

    print(f"\n{len(fotos)} fotos.  {total_antes/1024/1024:.1f} MB -> "
          f"{total_despues/1024/1024:.1f} MB  "
          f"({100 - total_despues/max(total_antes,1)*100:.0f} % menos)")
    print(f"Listas en: {destino}")

if __name__ == "__main__":
    main()
