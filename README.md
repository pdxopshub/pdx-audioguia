# Audioguía — Paradox Museum Barcelona

Guía interactiva para los visitantes del museo. Se abre escaneando un QR.
Web estática: no tiene servidor, ni base de datos, ni costes.

---

## Qué hay aquí

```
index.html              la app entera (textos, recorrido, estilos)
manifest.webmanifest    para que se pueda instalar como app
sw.js                   caché: funciona sin cobertura en el sótano
img/logo.png            logo de cabecera
img/icon-*.png          iconos de la app
img/fotos/              AQUÍ van las fotos de las exhibiciones
tools/optimizar-fotos.py  comprime las fotos antes de subirlas
```

---

## Publicar en GitHub Pages

1. Crea un repositorio **público** en GitHub, por ejemplo `pdx-audioguia`.
2. Sube todo el contenido de esta carpeta a la raíz del repositorio.
3. En el repositorio: **Settings → Pages**.
4. En *Source* elige **Deploy from a branch**, rama `main`, carpeta `/ (root)`.
5. Guarda. En un par de minutos la web está en
   `https://TU-USUARIO.github.io/pdx-audioguia/`

Para un dominio propio (`guia.paradoxmuseum.com`): añádelo en esa misma
pantalla de Pages, en *Custom domain*, y crea en tu proveedor de dominios
un registro `CNAME` que apunte a `TU-USUARIO.github.io`.

---

## Cada vez que publiques un cambio

Abre `sw.js` y sube el número de versión:

```js
const VERSION = "pdx-guia-v2";   // v1 -> v2 -> v3 ...
```

Si no lo haces, los móviles que ya entraron seguirán viendo la versión
antigua guardada en su caché. Es el fallo más habitual y el más molesto
de detectar.

---

## Las fotos

Van en `img/fotos/` en formato **WebP**. No subas JPG de la cámara
directamente: una foto de móvil pesa 3–5 MB y la guía tiene más de
cincuenta exhibiciones.

Para convertirlas:

```bash
python3 tools/optimizar-fotos.py ~/Escritorio/fotos-originales
```

Deja los WebP ya listos en `img/fotos/`. Los originales no se tocan.

**Cómo nombrarlas** (así se sabe a qué exhibición va cada una):

```
52_paradox-challenge_hero.jpg    la imagen principal de la ficha
52_paradox-challenge_paso1.jpg   cómo hacerla bien, paso 1
52_paradox-challenge_paso2.jpg   paso 2
32_ames-room_hero.jpg
32_ames-room_paso1.jpg
```

El número es el de la pared. Para las exhibiciones sin número, usa el
nombre a secas (`escape_hero.jpg`).

**Tamaños.** El script ya los aplica: 1200 px de ancho para las `_hero`
y 800 px para los pasos, calidad 80. Con eso una foto queda entre 30 KB
y 120 KB según el detalle que tenga, y se ve bien en cualquier móvil.
Si quieres apurar más, baja `CALIDAD` a 72 dentro del script.

---

## Cuánto consume

GitHub Pages da 100 GB al mes y es un límite blando: si se pasa, GitHub
avisa por correo en vez de apagar la web.

La app sin fotos pesa unos 65 KB. Un visitante que abra quince
exhibiciones se descarga alrededor de 1 MB en total, porque las fotos
sólo se cargan cuando abre esa ficha concreta. A ese ritmo harían falta
unas cien mil visitas al mes para acercarse al límite.

---

## Lo que falta

- [ ] Fotos reales de cada exhibición
- [ ] Textos definitivos de "El truco" y "Cómo hacerla bien"
- [ ] Ilustraciones en el estilo elegido
- [ ] QR definitivo apuntando a la URL final
