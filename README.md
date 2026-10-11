# La Llum del Pessebre — Descàrregues

Fitxers de descàrrega de la web **[lallumdelpessebre.cat](https://lallumdelpessebre.cat/)**.
Tots els botons "Descarregar" de la web apunten a aquest repositori.

## ARDMX (2026) — versió actual

| Fitxer | Descripció | Versió |
|---|---|---|
| [ARDMX/Manual_APP_ARDMX_CAT.pdf](ARDMX/Manual_APP_ARDMX_CAT.pdf) | Manual de l'APP ARDMX (català) | 3.0 |
| [ARDMX/Manual_APP_ARDMX_CAST.pdf](ARDMX/Manual_APP_ARDMX_CAST.pdf) | Manual de la APP ARDMX (castellano) | 3.0 |
| [ARDMX/Firmware_ARDMX_One.zip](ARDMX/Firmware_ARDMX_One.zip) | Instal·lador del firmware ARDMX One per a Windows (instruccions a LLEGEIX-ME.txt) | v2.2 |
| [ARDMX/Firmware_ARDMX_EVO.zip](ARDMX/Firmware_ARDMX_EVO.zip) | Instal·lador del firmware ARDMX EVO per a Windows (instruccions a LLEGEIX-ME.txt) | v2.1 |
| [ARDMX/Codi_ARDMX_One.zip](ARDMX/Codi_ARDMX_One.zip) | Codi font del firmware ARDMX One (projecte PlatformIO) | v2.2 |
| [ARDMX/Codi_ARDMX_EVO.zip](ARDMX/Codi_ARDMX_EVO.zip) | Codi font del firmware ARDMX EVO (projecte PlatformIO) | v2.1 |

## Normes del repositori

- Una carpeta per secció de la web: `ARDMX/`, `ARDMX4/`, `ARDMX2/`, `ARDMX1/`, `Cursos/`…
- Els noms dels fitxers **no** porten número de versió, perquè els enllaços de la web
  no canviïn quan s'actualitzen. La versió vigent s'indica en aquest README.
- Enllaç de descàrrega directa des de la web:
  `https://github.com/xaviermila-png/lallumdelpessebre/raw/refs/heads/main/<carpeta>/<fitxer>`

## Origen dels fitxers

- Els ZIP de firmware es generen a partir de la carpeta `installer_standalone/` de
  [ardmx-one-firmware](https://github.com/xaviermila-png/ardmx-one-firmware) i
  [ardmx-evo-firmware](https://github.com/xaviermila-png/ardmx-evo-firmware).
- Els ZIP de codi (`Codi_*.zip`) contenen `src/`, `platformio.ini`, `partitions.csv`,
  `README.md` i `LICENSE` dels mateixos repositoris.
  Quan surti una versió nova del firmware, cal tornar a generar el ZIP i actualitzar la versió d'aquesta taula.
