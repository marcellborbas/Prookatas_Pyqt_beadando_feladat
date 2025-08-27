# Library - Könyvtárkezelő alkalmazás

Ez egy egyszerű, PyQt6-alapú könyvtárkezelő asztali alkalmazás, amely támogatja a felhasználói regisztrációt, könyvek kölcsönzését, adminisztrációs funkciókat, toplistákat és statisztikákat.

## Telepítési útmutató (Pycharm alatt)

1. **Python telepítése**  
   Győződj meg róla, hogy Python (3.9 vagy újabb) telepítve van.

2. **Virtuális környezet létrehozása**  
   Pycharm automatikusan létrehozza, vagy terminálban:
   ```sh
   python -m venv venv
   ```

3. **Szükséges csomagok telepítése**  
   Nyisd meg a terminált a projekt mappájában, és futtasd:
   ```sh
   pip install pyqt6 matplotlib
   ```

## Futtatás

1. Nyisd meg a projektet Pycharm-ban.
2. Futtasd a `main.py` fájlt.
3. Az alkalmazás első induláskor létrehozza az adatbázist (`library.db`).

## Egyéb teendők

1. A pdf_tesztelesehez_konyvek.csv fájlba ne felejtsd el be másolni a pdf fájlok absolute_path -át

## Fő funkciók

- **Regisztráció, bejelentkezés, profil szerkesztés**
- **Könyvek böngészése, szűrése, kölcsönzése, visszaadása**
- **Könyvek értékelése, véleményezése**
- **Könyvek toplistája, olvasók toplistája**
- **Könyvek keresés eredményeinek exportálása**
- **Adminisztráció: felhasználók kezelése, könyvek importálása CSV-ből**
- **Profilkép feltöltés**

## Felhasználói szerepkörök

- **Admin:** könyvek/olvasók kezelése, import, kategória kezelés
- **Felhasználó:** könyvek böngészése, kölcsönzés/visszaadás, értékelés

## Jegyzetek

- A projekt SQLite adatbázist használ (`library.db` a projekt gyökerében).
- Profilképekhez helyi fájl elérési utat ment.
- A fejlesztéshez ajánlott legalább Python 3.9 és Pycharm CE vagy Professional.

---

**Jó használatot kívánok!**