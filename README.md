# La Llum del Pessebre — Descàrregues

Fitxers de descàrrega de la web **[lallumdelpessebre.cat](https://lallumdelpessebre.cat/)**.
Tots els botons "Descarregar" de la web apunten a aquest repositori.

## ARDMX (2026) — versió actual

| Fitxer | Descripció | Versió | Data |
|---|---|---|---|
| [ARDMX/Manual_APP_ARDMX_CAT.pdf](ARDMX/Manual_APP_ARDMX_CAT.pdf) | Manual de l'APP ARDMX (català) | 3.0 | |
| [ARDMX/Manual_APP_ARDMX_CAST.pdf](ARDMX/Manual_APP_ARDMX_CAST.pdf) | Manual de la APP ARDMX (castellano) | 3.0 | |
| [ARDMX/Firmware_ARDMX_One.zip](ARDMX/Firmware_ARDMX_One.zip) | Firmware ARDMX One: instal·lador per a Windows (instruccions a LLEGEIX-ME.txt) i codi font a `Codi_font/` | v2.2 | compilat el 13/09/2026 |
| [ARDMX/Firmware_ARDMX_EVO.zip](ARDMX/Firmware_ARDMX_EVO.zip) | Firmware ARDMX EVO: instal·lador per a Windows (instruccions a LLEGEIX-ME.txt) i codi font a `Codi_font/` | v2.1 | compilat el 13/09/2026 |

## ARDMX1 (2021)

| Fitxer | Descripció | Versió |
|---|---|---|
| [ARDMX1/Programa_ARDMX1.txt](ARDMX1/Programa_ARDMX1.txt) | Programa en C++ de l'ARDMX1 per a l'Arduino Mega 2560 | v1.5 |

## Cursos

| Fitxer | Descripció | Data |
|---|---|---|
| [Cursos/Xerrada_Tarragona_2026.pdf](Cursos/Xerrada_Tarragona_2026.pdf) | Presentació de la xerrada col·loqui sobre il·luminació de pessebres, Associació Pessebrista de Tarragona | 11/07/2026 |
| [Cursos/Curs_DMX_Vilanova_2026.pdf](Cursos/Curs_DMX_Vilanova_2026.pdf) | Presentació del curs d'il·luminació amb DMX, Associació Pessebrista de Vilanova i la Geltrú | 19/06/2026 |

## Normes del repositori

- Una carpeta per secció de la web: `ARDMX/`, `ARDMX4/`, `ARDMX2/`, `ARDMX1/`, `Cursos/`…
- Els noms dels fitxers **no** porten número de versió, perquè els enllaços de la web
  no canviïn quan s'actualitzen. La versió vigent s'indica en aquest README.
- Enllaç de descàrrega directa des de la web:
  `https://github.com/xaviermila-png/lallumdelpessebre/raw/refs/heads/main/<carpeta>/<fitxer>`

## Origen dels fitxers

- Els ZIP de firmware es generen amb `python3 eines/genera_zip_firmware.py <ardmx-one-firmware> <ardmx-evo-firmware>`.
  Contenen la carpeta `installer_standalone/` de
  [ardmx-one-firmware](https://github.com/xaviermila-png/ardmx-one-firmware) i
  [ardmx-evo-firmware](https://github.com/xaviermila-png/ardmx-evo-firmware),
  més una subcarpeta `Codi_font/` amb `src/`, `platformio.ini`, `partitions.csv`,
  `README.md` i `LICENSE` del mateix repositori, i un `LLEGEIX-ME.txt` propi (definit a l'script)
  que explica les dues parts. **No** s'hi inclou `update_*.bat`: l'únic camí és `install_*.bat`,
  que esborra tota la configuració i deixa el controlador de fàbrica.
  Quan surti una versió nova del firmware, cal tornar a generar el ZIP i actualitzar la versió i la data d'aquesta taula
  (l'script les llegeix de `bin/version.txt` de l'instal·lador).
