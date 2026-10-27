#!/usr/bin/env python3
"""Genera els ZIP de l'instal·lador de firmware per adjuntar a les Releases de GitHub.

Surt un ZIP per controlador, amb el mateix nom que fan servir els botons de la web
(https://github.com/xaviermila-png/ardmx-<x>-firmware/releases/latest/download/<nom>):

  ardmx_one_instal-lador.zip   (repositori ardmx-one-firmware)
  ardmx_evo_instal-lador.zip   (repositori ardmx-evo-firmware)

Cada ZIP té una carpeta arrel ARDMX_<Nom>_<versió>/ amb l'instal·lador autònom
per a Windows (carpeta installer_standalone/ del repositori de firmware) i un
LLEGEIX-ME.txt generat aquí. El codi font NO hi va: GitHub l'afegeix sol a cada
Release («Source code (zip)»).

Els instal·ladors són només per a Windows: les rutes del ZIP fan servir «\\» i els
fitxers de text van amb salts de línia CRLF.

No s'hi inclou update_*.bat: l'únic camí d'instal·lació és install_*.bat,
que esborra tota la memòria de la placa i la deixa de fàbrica.

Ús:
  python3 eines/genera_zip_firmware.py <ruta ardmx-one-firmware> <ruta ardmx-evo-firmware> <carpeta de sortida>
"""
import sys
import zipfile
from pathlib import Path

TEXT = {".bat", ".ps1", ".txt"}

CONTROLADORS = {
    "One": {
        "fitxer": "one",
        "config": "canals, escenes, transicions, pessebre, descripció, nom Bluetooth, PIN",
        "export": "canals, escenes, transicions, pessebre i descripció",
        "avis_v1": (
            "IMPORTANT: aquest firmware és només per a l'ARDMX One v2 (Bluetooth\n"
            "Low Energy, 4 escenes). NO l'instal·lis en un ARDMX One v1 (Bluetooth\n"
            "Classic, una sola escena): els v1 es mantenen amb el seu firmware original.\n\n"
        ),
    },
    "EVO": {
        "fitxer": "evo",
        "config": "canals, escenes, events, pessebre, nom Bluetooth, PIN",
        "export": "canals, escenes, events, pessebre i descripció",
        "avis_v1": "",
    },
}

PLANTILLA = """\
ARDMX {nom} — Firmware {versio} (compilat el {data})
{subratllat}

Aquest paquet posa el programa (firmware) a la placa ESP32 de l'ARDMX {nom}
des d'un ordinador amb Windows, sense haver d'instal·lar res més (ni
Python, ni PlatformIO, ni Arduino IDE).

{avis_v1}Abans de començar
-----------------
1. Descomprimeix el ZIP a qualsevol carpeta de l'ordinador (per exemple
   a l'Escriptori). No l'executis des de dins del ZIP.
2. Connecta la placa ESP32 a l'ordinador amb un cable USB.
   El cable ha de ser de DADES, no només de càrrega.

Molt important: la instal·lació ho esborra tot
-----------------------------------------------
L'instal·lador esborra tota la memòria de la placa i la deixa com nova de
fàbrica: instal·la el programa i ESBORRA TOTA la configuració desada
({config}).

Si vols conservar la configuració, ABANS d'instal·lar fes una EXPORTACIÓ
des del menú Eines de l'APP ARDMX (Eines -> Exportar, fitxer JSON). Després
de la instal·lació la pots IMPORTAR (Eines -> Importar) per recuperar
{export}.
El nom Bluetooth i el PIN no s'exporten: els hauràs de tornar a posar a
mà si els havies canviat.

Passos
------
1. Dins la carpeta descomprimida, fes doble clic a install_ardmx_{fitxer}.bat
2. S'obre una finestra negra amb la versió que s'instal·larà i la llista
   de ports COM. Si detecta l'ESP32, en recomana un (per exemple "COM10"):
   prem Enter per fer-lo servir, o escriu un altre port i prem Enter.
3. Llegeix l'avís que la placa s'esborrarà i respon "s" per continuar
   (qualsevol altra resposta cancel·la).
4. Espera unes desenes de segons. NO desendollis el cable mentre treballa.
5. Al final ha de sortir "Firmware instal·lat correctament".
   Prem una tecla per tancar.
6. Connecta't des de l'APP ARDMX i configura el controlador (o importa
   la configuració que havies exportat).

Si hi ha algun error
--------------------
- Comprova que el cable USB sigui de dades (n'hi ha que només carreguen).
- Comprova que el port COM sigui el correcte (torna a executar el .bat i
  mira la llista de ports).
- Si Windows no reconeix la placa, pot caldre el controlador del xip
  USB-sèrie (normalment CH340): cerca "driver CH340" al navegador.
- No separis el .bat de la resta de fitxers: esptool.exe, detect_port.ps1
  i la carpeta bin són necessaris.

Codi font i versions anteriors
------------------------------
{repo}/releases

Més informació: https://lallumdelpessebre.cat
"""


def versio(installer: Path) -> tuple[str, str]:
    """Llegeix bin/version.txt -> ("v2.2", "13/09/2026")."""
    linies = (installer / "bin" / "version.txt").read_text(encoding="utf-8").splitlines()
    ver = linies[0].split()[-1]  # "ARDMX One v2.2" -> "v2.2"
    data = next(l for l in linies if l.startswith("Generat:")).split()[-1]  # "2026-09-13"
    a, m, d = data.split("-")
    return ver, f"{d}/{m}/{a}"


def crlf(dades: bytes) -> bytes:
    return dades.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")


def genera(nom: str, repo_fw: Path, sortida: Path) -> Path:
    cfg = CONTROLADORS[nom]
    inst = repo_fw / "installer_standalone"
    ver, data = versio(inst)
    arrel = f"ARDMX_{nom}_{ver}"
    titol = f"ARDMX {nom} — Firmware {ver} (compilat el {data})"
    llegeix = PLANTILLA.format(
        nom=nom, versio=ver, data=data, subratllat="=" * len(titol),
        repo=f"https://github.com/xaviermila-png/ardmx-{cfg['fitxer']}-firmware", **cfg
    )

    desti = sortida / f"ardmx_{cfg['fitxer']}_instal-lador.zip"
    with zipfile.ZipFile(desti, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(inst.rglob("*")):
            if f.is_file() and f.name != "LLEGEIX-ME.txt" and not f.name.startswith("update_"):
                dades = f.read_bytes()
                if f.suffix.lower() in TEXT:
                    dades = crlf(dades)
                ruta = "\\".join((arrel, *f.relative_to(inst).parts))
                z.writestr(ruta, dades)
        z.writestr(f"{arrel}\\LLEGEIX-ME.txt", crlf(llegeix.encode("utf-8")))
    print(f"{desti}  ({ver}, compilat el {data})")
    return desti


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sortida = Path(sys.argv[3])
    sortida.mkdir(parents=True, exist_ok=True)
    genera("One", Path(sys.argv[1]), sortida)
    genera("EVO", Path(sys.argv[2]), sortida)
