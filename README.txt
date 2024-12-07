
# README : Script de Vérification d'Adresses et Soldes Crypto

## Description

Ce script génère aléatoirement des **seed phrases**, dérive des adresses sur plusieurs blockchains (Ethereum, Bitcoin, Solana, Polygon, Binance Smart Chain, et Base), et affiche les soldes associés. Les wallets contenant des fonds sont sauvegardés dans un fichier texte pour une analyse ultérieure.

---

## Prérequis

1. **Python** (version 3.8 ou supérieure)
   - Assurez-vous que Python est installé sur votre machine. Si ce n'est pas le cas :
     - **Windows** : Téléchargez-le depuis [python.org](https://www.python.org/downloads/) et suivez les instructions d'installation.
     - **macOS** : Installez Python avec Homebrew (`brew install python`) ou téléchargez-le depuis le site officiel.
     - **Linux** : Installez Python via le gestionnaire de paquets de votre distribution :
       ```bash
       sudo apt update && sudo apt install python3 python3-pip -y  # Debian/Ubuntu
       sudo dnf install python3 python3-pip -y                    # Fedora
       ```

2. **pip**
   - pip est l'outil de gestion des dépendances Python. Il est normalement inclus avec Python 3. Si ce n'est pas le cas :
     ```bash
     python3 -m ensurepip --upgrade
     ```

---

## Installation des dépendances

Avant d'exécuter le script, installez les bibliothèques nécessaires. Elles sont listées dans le fichier `requirements.txt`.

### Étapes :
1. **Téléchargez ou clonez ce projet dans un répertoire de votre choix.**
2. **Ouvrez un terminal/une invite de commandes et naviguez dans le répertoire du projet.**
3. **Installez les dépendances avec pip** :
   ```bash
   pip install -r requirements.txt
   ```

### Contenu du fichier `requirements.txt` :
```
bip-utils
web3
rich
requests
pyfiglet
```

---

## Instructions par système d'exploitation

### **Windows**
1. **Installer Python** :
   - Téléchargez Python depuis [python.org](https://www.python.org/downloads/).
   - Pendant l'installation, cochez la case **"Add Python to PATH"**.
2. **Installer les dépendances** :
   - Ouvrez PowerShell ou l'Invite de commandes.
   - Naviguez dans le dossier du script :
     ```bash
     cd chemin\vers\le\dossier
     ```
   - Installez les dépendances :
     ```bash
     pip install -r requirements.txt
     ```
3. **Exécuter le script** :
   ```bash
   python script.py
   ```

---

### **macOS**
1. **Installer Python** :
   - Utilisez Homebrew pour installer Python si non installé :
     ```bash
     brew install python
     ```
2. **Installer les dépendances** :
   - Ouvrez le terminal.
   - Naviguez dans le dossier du script :
     ```bash
     cd /chemin/vers/le/dossier
     ```
   - Installez les dépendances :
     ```bash
     pip install -r requirements.txt
     ```
3. **Exécuter le script** :
   ```bash
   python3 script.py
   ```

---

### **Linux**
1. **Installer Python** :
   - Utilisez le gestionnaire de paquets approprié pour votre distribution. Par exemple :
     ```bash
     sudo apt update && sudo apt install python3 python3-pip -y  # Debian/Ubuntu
     ```
2. **Installer les dépendances** :
   - Ouvrez un terminal.
   - Naviguez dans le dossier du script :
     ```bash
     cd /chemin/vers/le/dossier
     ```
   - Installez les dépendances :
     ```bash
     pip install -r requirements.txt
     ```
3. **Exécuter le script** :
   ```bash
   python3 script.py
   ```

---

## Structure des fichiers générés

- **`wallets_found.txt`** : Contient les informations sur les wallets avec des fonds suffisants.
  - Format :
    ```
    Portefeuille #1 trouvé:
    Seed Phrase: [phrase ici]
    Ethereum Adresse: [adresse ici]
    Ethereum Solde: [solde ici]

    ==========================
    ```

---

## Notes supplémentaires

- **Problèmes fréquents** :
  1. **Erreur de connexion RPC** : Vérifiez votre connexion Internet et l'état des nœuds blockchain.
  2. **Permission refusée** : Assurez-vous d'avoir les droits pour exécuter des scripts sur votre système.
  3. **Modules manquants** : Si une dépendance est manquante, réexécutez :
     ```bash
     pip install -r requirements.txt
     ```

- **Pour arrêter le script en cours d'exécution**, utilisez :
  - Windows : `Ctrl + C`
  - macOS/Linux : `Ctrl + C`

---

## Avertissement

Ce script est conçu à des fins éducatives. L'utilisation abusive ou illégale de ce script est strictement interdite. L'auteur décline toute responsabilité pour tout usage non conforme aux lois locales.

---

## Auteur

Créé par : Neo 
Contact : TG: @Neo_bi | Twitter: @NEO_B_I
