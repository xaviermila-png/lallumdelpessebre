#!/usr/bin/env python3
"""Genera ARDMX/Firmware_ARDMX_One.zip i ARDMX/Firmware_ARDMX_EVO.zip.

Cada ZIP conté:
  - l'instal·lador autònom per a Windows (carpeta installer_standalone/ del
    repositori de firmware),
  - el codi font a la subcarpeta Codi_font/ (src/, platformio.ini,
    partitions.csv, README.md, LICENSE),
  - un LLEGEIX-ME.txt generat aquí, que substitueix el de l'instal·lador.

Ús:
  python3 eines/genera_zip_firmware.py <ruta ardmx-one-firmware> <ruta ardmx-evo-firmware>
"""
import io
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FONT = ["src", "platformio.ini", "partitions.csv", "README.md", "LICENSE"]

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
ARDMX {nom} — Firmware {versio}
{subratllat}

Aquest ZIP conté dues coses:

  1. L'INSTAL·LADOR per a Windows (els fitxers d'aquesta carpeta).
     Serveix per posar el programa a la placa ESP32 de l'ARDMX {nom}
     sense haver d'instal·lar res més a l'ordinador (ni Python, ni
     PlatformIO, ni Arduino IDE). És el que necessita la majoria de gent.

  2. El CODI FONT (carpeta Codi_font). És el programa en C++ a partir
     del qual s'ha generat l'instal·lador. Només cal si vols estudiar-lo,
     modificar-lo o compilar-lo tu mateix. Per instal·lar el firmware
     NO el necessites.

{avis_v1}Abans de començar
-----------------
1. Descomprimeix el ZIP a qualsevol carpeta de l'ordinador (per exemple
   a l'Escriptori). No l'executis des de dins del ZIP.
2. Connecta la placa ESP32 a l'ordinador amb un cable USB.
   El cable ha de ser de DADES, no només de càrrega.

Tria quin fitxer has d'executar
-------------------------------
A) ACTUALITZAR un ARDMX {nom} que ja funciona → update_ardmx_{fitxer}.bat
   Només canvia el programa per la versió nova. La configuració desada
   ({config})
   es queda tal com està.
   És l'opció recomanada per a un dispositiu que ja tens configurat.

B) INSTAL·LACIÓ NETA (placa nova o deixar-la com de fàbrica)
   → install_ardmx_{fitxer}.bat
   Instal·la el programa i ESBORRA TOTA la configuració desada
   ({config}).
   Si vols conservar-la, abans fes una EXPORTACIÓ des de la pantalla
   "Configuració" de l'APP ARDMX (fitxer JSON). Després de la instal·lació
   la pots IMPORTAR per recuperar {export}.
   El nom Bluetooth i el PIN no s'exporten: els hauràs de tornar a posar
   a mà si els havies canviat.

Passos (iguals per a A i B)
---------------------------
1. Fes doble clic al fitxer .bat que hagis triat.
2. S'obre una finestra negra amb la versió que s'instal·larà i la llista
   de ports COM. Si detecta l'ESP32, en recomana un (per exemple "COM10"):
   prem Enter per fer-lo servir, o escriu un altre port i prem Enter.
3. Llegeix l'avís i respon "s" per continuar.
4. Espera unes desenes de segons. NO desendollis el cable mentre treballa.
5. Al final ha de sortir "Firmware instal·lat correctament" (opció B) o
   "Firmware actualitzat correctament" (opció A). Prem una tecla per tancar.

Si hi ha algun error
--------------------
- Comprova que el cable USB sigui de dades.
- Comprova que el port COM sigui el correcte (torna a executar el .bat i
  mira la llista de ports).
- Si Windows no reconeix la placa, pot caldre el controlador del xip
  USB-sèrie (normalment CH340): cerca "driver CH340" al navegador.
- No separis el .bat de la resta de fitxers: esptool.exe, detect_port.ps1
  i la carpeta bin són necessaris.

Codi font (carpeta Codi_font)
-----------------------------
- src/main.cpp     programa complet de l'ESP32
- platformio.ini   configuració del projecte PlatformIO
- partitions.csv   taula de particions de la memòria de l'ESP32
- README.md        documentació tècnica: maquinari, connexions i com
                   compilar
- LICENSE          llicència del codi

Per compilar-lo: obre la carpeta Codi_font amb Visual Studio Code i
l'extensió PlatformIO, i fes Build i Upload (detall al README.md).
Pujar-lo des de PlatformIO no esborra la configuració desada.

Més informació: https://lallumdelpessebre.cat
"""


def versio(installer: Path) -> str:
    primera = (installer / "bin" / "version.txt").read_text(encoding="utf-8").splitlines()[0]
    return primera.split()[-1]  # "ARDMX One v2.2" -> "v2.2"


def genera(nom: str, repo_fw: Path) -> Path:
    cfg = CONTROLADORS[nom]
    inst = repo_fw / "installer_standalone"
    ver = versio(inst)
    arrel = f"Firmware_ARDMX_{nom}"
    titol = f"ARDMX {nom} — Firmware {ver}"
    llegeix = PLANTILLA.format(
        nom=nom, versio=ver, subratllat="=" * len(titol), **cfg
    ).replace("\n", "\r\n")

    desti = REPO / "ARDMX" / f"{arrel}.zip"
    with zipfile.ZipFile(desti, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(inst.rglob("*")):
            if f.is_file() and f.name != "LLEGEIX-ME.txt":
                z.write(f, f"{arrel}/{f.relative_to(inst).as_posix()}")
        z.writestr(f"{arrel}/LLEGEIX-ME.txt", llegeix.encode("utf-8"))
        tar = subprocess.run(
            ["git", "-C", str(repo_fw), "archive", "--format=tar", "HEAD", *FONT],
            check=True, capture_output=True,
        ).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            for m in t.getmembers():
                if m.isfile():
                    z.writestr(f"{arrel}/Codi_font/{m.name}", t.extractfile(m).read())
    print(f"{desti.relative_to(REPO)}  ({ver})")
    return desti


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    genera("One", Path(sys.argv[1]))
    genera("EVO", Path(sys.argv[2]))
