import os
import random
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicGenerator
from web3 import Web3
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import pyfiglet  # Importation de pyfiglet pour les titres


# Configuration de l'interface
console = Console()

# URLs RPC pour les blockchains (Mainnet uniquement)
RPC_URLS = {
    "ethereum": "https://rpc.flashbots.net",
    "bsc": "https://bsc-dataseed.binance.org/",
    "polygon": "https://polygon-rpc.com/",
    "solana": "https://api.mainnet-beta.solana.com",
    "base": "https://mainnet.base.org"
}

# Seuils minimaux pour chaque réseau (en fonction de la plus petite unité de chaque réseau)
seuil_minimal = {
    "ethereum": 0.00000001,
    "bsc": 0.00000001,
    "polygon": 0.00000001,
    "solana": 0.00000001,
    "bitcoin": 0.00000001,
    "base": 0.00000001
}

# Fonction pour dériver les adresses Ethereum, Bitcoin, Solana, Polygon et BASE
def derive_addresses(seed_phrase):
    seed_generator = Bip39SeedGenerator(seed_phrase)
    seed = seed_generator.Generate()

    # Ethereum
    bip44_eth = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    eth_wallet = bip44_eth.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    eth_address = eth_wallet.PublicKey().ToAddress()

    # Bitcoin
    bip44_btc = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    btc_wallet = bip44_btc.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    btc_address = btc_wallet.PublicKey().ToAddress()

    # Solana
    bip44_solana = Bip44.FromSeed(seed, Bip44Coins.SOLANA)
    solana_wallet = bip44_solana.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    solana_address = solana_wallet.PublicKey().ToAddress()

    # Polygon
    bip44_polygon = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    polygon_wallet = bip44_polygon.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    polygon_address = polygon_wallet.PublicKey().ToAddress()

    # BASE
    bip44_base = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    base_wallet = bip44_base.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    base_address = base_wallet.PublicKey().ToAddress()

    return eth_address, btc_address, solana_address, polygon_address, base_address

# Fonction pour vérifier les soldes
def check_eth_balance(address, rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        return 0  # Retourne 0 en cas de non-connectivité
    try:
        balance = web3.eth.get_balance(address)
        return float(web3.from_wei(balance, 'ether'))
    except Exception as e:
        return 0

def check_bsc_balance(address, rpc_url):
    return check_eth_balance(address, rpc_url)

def check_btc_balance(address):
    url = f"https://blockstream.info/api/address/{address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = data["chain_stats"]["funded_txo_sum"] - data["chain_stats"]["spent_txo_sum"]
        return balance / 1e8
    except Exception as e:
        return 0

def check_solana_balance(address, rpc_url):
    headers = {"Content-Type": "application/json"}
    data = {"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [address]}
    try:
        response = requests.post(rpc_url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("result", {}).get("value", 0) / 1e9
    except Exception as e:
        return 0

def check_polygon_balance(address, rpc_url):
    return check_eth_balance(address, rpc_url)

def check_base_balance(address, rpc_url):
    return check_eth_balance(address, rpc_url)

# Fonction pour vérifier la connectivité RPC
def test_rpc_connectivity(rpc_urls):
    console.print(Panel("[bold cyan]Test des connectivités RPC :[/bold cyan]", title="Test RPC", subtitle="Vérification de la connectivité aux nœuds", style="bold cyan"))
    for chain, rpc_url in rpc_urls.items():
        try:
            response = requests.post(rpc_url, json={"jsonrpc": "2.0", "method": "web3_clientVersion", "params": [], "id": 1}, timeout=5)
            response.raise_for_status()
            console.print(f"[bold green]{chain.capitalize()} : Connecté avec succès ![/bold green]")
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]{chain.capitalize()} : Erreur - {e}[/bold red]")

# Fonction pour tester les adresses générées
def test_addresses(addresses, rpc_urls):
    results = {}
    for network, (address, rpc_url) in addresses.items():
        if network in ["ethereum", "bsc", "polygon", "base"]:
            balance = check_eth_balance(address, rpc_url)
        elif network == "bitcoin":
            balance = check_btc_balance(address)
        elif network == "solana":
            balance = check_solana_balance(address, rpc_url)
        else:
            balance = 0
        results[network] = (address, balance if isinstance(balance, (int, float)) else 0)
    return results


# Fonction pour sauvegarder uniquement les wallets valides dans des fichiers séparés

def save_wallet_info_if_minimum_reached(wallet_info, seed_phrase, counter):
    has_valid_wallet = False

    # Utiliser l'adresse Ethereum comme nom de fichier
    eth_address = wallet_info.get('ethereum', ('', 0))[0]  # Récupère l'adresse Ethereum
    if eth_address:
        file_name = f"wallet_{eth_address}_details.txt"  # Nom du fichier basé sur l'adresse Ethereum
    else:
        file_name = f"wallet_{counter}_details.txt"  # Si l'adresse est vide, utiliser le compteur par défaut

    with open(file_name, "w") as file:
        file.write(f"==== Détails du Portefeuille #{counter} ====\n")
        file.write(f"Seed Phrase: {seed_phrase}\n\n")
        file.write("Adresses et soldes associés :\n")

        for network, (address, balance) in wallet_info.items():
            balance_str = f"{balance} {network.capitalize()}" if isinstance(balance, (int, float)) else "Erreur lors de la récupération du solde"
            file.write(f"- {network.capitalize()} :\n")
            file.write(f"  Adresse : {address}\n")
            file.write(f"  Solde   : {balance_str}\n\n")

            # Vérifier si le seuil est dépassé
            if isinstance(balance, (int, float)) and balance >= seuil_minimal.get(network, 0):
                has_valid_wallet = True

    if has_valid_wallet:
        console.print(f"[bold green]Portefeuille #{counter} avec des fonds trouvé et sauvegardé dans {file_name}[/bold green]")
        
    else:
        os.remove(file_name)  # Supprime le fichier si aucun solde valide n'est trouvé
        console.print(f"[yellow]Portefeuille #{counter} enregistré, mais sans fonds suffisants. Fichier supprimé.[/yellow]")



# Fonction principale
def main():
    title = pyfiglet.figlet_format("NEO B CHECK WALLETS", font="slant")
    console.print(f"[bold cyan]{title}[/bold cyan]")

    # Tester les connectivités RPC
    test_rpc_connectivity(RPC_URLS)

    # Demander à l'utilisateur de choisir entre une seed fixe ou génération infinie
    console.print(Panel("[bold cyan]Souhaitez-vous utiliser une seed phrase existante ou en générer aléatoirement en boucle ?[/bold cyan]", style="bold cyan"))
    console.print("[1] Entrer une seed phrase manuellement")
    console.print("[2] Générer des seed phrases aléatoires en boucle")
    choice = input("Votre choix (1/2) : ").strip()

    if choice == "1":
        seed_phrase = input("Entrez votre seed phrase : ").strip()
        process_seed(seed_phrase, counter=1)
    elif choice == "2":
        console.print("[bold green]Génération infinie de seed phrases aléatoires...[/bold green]")
        try:
            counter = 1
            mnemonic_generator = Bip39MnemonicGenerator()
            while True:
                seed_phrase = mnemonic_generator.FromWordsNumber(12)  # Génère une seed phrase de 12 mots
                console.print(f"\n[bold yellow]Seed phrase #{counter} :[/bold yellow] {seed_phrase}")
                process_seed(seed_phrase, counter)
                counter += 1
        except KeyboardInterrupt:
            console.print("\n[bold cyan]Interruption par l'utilisateur. Fin du programme.[/bold cyan]")
    else:
        console.print("[bold red]Choix invalide, veuillez relancer le programme.[/bold red]")


def process_seed(seed_phrase, counter):
    """Processus de vérification d'une seed phrase."""
    eth_address, btc_address, solana_address, polygon_address, base_address = derive_addresses(seed_phrase)

    addresses = {
        "ethereum": (eth_address, RPC_URLS["ethereum"]),
        "bsc": (eth_address, RPC_URLS["bsc"]),
        "bitcoin": (btc_address, None),
        "solana": (solana_address, RPC_URLS["solana"]),
        "polygon": (polygon_address, RPC_URLS["polygon"]),
        "base": (base_address, RPC_URLS["base"])
    }

    results = test_addresses(addresses, RPC_URLS)

    # Afficher les résultats
    table = Table(title=f"DÉTAILS DES ADRESSES ET SOLDES (# {counter})", title_style="bold cyan")
    table.add_column("RÉSEAU", style="bold cyan", justify="center")
    table.add_column("ADRESSE", style="bold white")
    table.add_column("RÉPONSE API / SOLDE", style="bold cyan", justify="right")

    for network, (address, balance) in results.items():
        balance_str = f"{balance} {network}" if isinstance(balance, (int, float)) else f"[red]{balance}[/red]"
        table.add_row(network.capitalize(), address, balance_str)

    console.print(table)

    # Sauvegarder les portefeuilles avec des fonds
    save_wallet_info_if_minimum_reached(results, seed_phrase, counter)


if __name__ == "__main__":
    main()

