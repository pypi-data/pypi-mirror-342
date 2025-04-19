import subprocess
from rich.console import Console
from rich.table import Table
import pyfiglet
import os
import sys

console = Console()

def fichier_existe(fichier):
    return os.path.isfile(fichier)

def afficher_menu():
    """Affiche le menu principal avec style ASCII et tableau"""
    title = pyfiglet.figlet_format("Outil de\nCryptographie")
    console.print(f"[bold cyan]{title}[/bold cyan]")

    table = Table(title="[italic bold]Menu Principal[/italic bold]", show_header=True, header_style="bold magenta")
    table.add_column("Option", justify="center", style="cyan", no_wrap=True)
    table.add_column("Description", style="bold yellow")

    options = [
        ("1", "Génération de clé privée (RSA)"),
        ("2", "Chiffrement d'une clé privée (AES/3DES)"),
        ("3", "Génération de clé publique (RSA)"),
        ("4", "Chiffrement de données (RSA/AES/3DES)"),
        ("5", "Déchiffrement de données (RSA/AES/3DES)"),
        ("6", "Calcul d'empreinte (MD5/SHA256)"),
        ("7", "Signature d'empreinte (RSA)"),
        ("8", "Vérification de signature (RSA)"),
        ("99", "Quitter"),
    ]

    for opt, desc in options:
        table.add_row(opt, desc)

    console.print(table)

def executer_commande(cmd):
    """Exécute une commande shell et gère les erreurs"""
    try:
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Erreur OpenSSL : {e}[/red]")
    except FileNotFoundError:
        console.print("[red]Erreur : fichier introuvable.[/red]")

def gen_cle_pri():
    console.print("\n[bold yellow]Génération de clé privée[/bold yellow]")
    file_name = input("Nom de la clé privée : ")
    cmd = f"openssl genpkey -algorithm RSA -out {file_name} -pkeyopt rsa_keygen_bits:2048"
    executer_commande(cmd)
    console.print(f"[green]{file_name} créé avec succès ![/green]")

def chif_cle():
    console.print("\n[bold yellow]Chiffrement de clé privée[/bold yellow]")
    file_in = input("Nom de la clé à chiffrer : ")
    if not fichier_existe(file_in):
        return console.print("[red]Fichier introuvable.[/red]")
    file_out = input("Nom du fichier chiffré en sortie : ")
    algo = input("Algorithme (aes256, des3) : ").lower()

    cmd = f"openssl pkey -in {file_in} -{algo} -out {file_out}"
    executer_commande(cmd)
    console.print("[green]Clé chiffrée avec succès.[/green]")

def gen_cle_pub():
    console.print("\n[bold yellow]Génération de clé publique[/bold yellow]")
    file_in = input("Clé privée : ")
    if not fichier_existe(file_in):
        return console.print("[red]Clé privée introuvable.[/red]")
    file_out = input("Nom de la clé publique : ")

    cmd = f"openssl pkey -in {file_in} -pubout -out {file_out}"
    executer_commande(cmd)
    console.print("[green]Clé publique générée avec succès.[/green]")

def chif_d():
    console.print("\n[bold yellow]Chiffrement de données[/bold yellow]")
    file_in = input("Fichier à chiffrer : ")
    if not fichier_existe(file_in):
        return console.print("[red]Fichier introuvable.[/red]")
    file_out = input("Nom du fichier chiffré : ")
    #algo = input("Algorithme (rsa, aes-256-cbc, des-ede3-cbc) : ").lower()
    algo = input("algorithme (RSA, AES-256, 3-DES) : ").upper()

    if algo == "RSA":
        cle_priv = input("Clé privé pour le chiffrement : ")
        if not fichier_existe(cle_priv):
            return console.print("[red]Clé privé introuvable.[/red]")

        cmd = f"openssl pkeyutl -encrypt -in {file_in} -pubin -inkey {cle_priv} -out {file_out}"
    #elif algo in ["aes-256-cbc", "des-ede3-cbc"]:
    elif algo in ["AES-256", "3-DES"]:
        if algo == "AES-256":
            cmd = f"openssl enc -aes-256-cbc -pbkdf2 -in {file_in} -out {file_out}"
        elif algo == "3-DES":
            cmd = f"openssl enc -des-ede3-cbc -pbkdf2 -in {file_in} -out {file_out}"
        #cmd = f"openssl enc -{algo} -pbkdf2 -in {file_in} -out {file_out}"
    else:
        console.print("[red]Algorithme non supporté.[/red]")
        return

    executer_commande(cmd)
    console.print("[green]Données chiffrées avec succès.[/green]")

def dechif_d():
    console.print("\n[bold yellow]Déchiffrement de données[/bold yellow]")
    file_in = input("Fichier à déchiffré : ")
    if not fichier_existe(file_in):
        return console.print("[red]Fichier introuvable.[/red]")
    file_out = input("Nom du fichier déchiffré : ")
    #algo = input("Algorithme (rsa, aes-256-cbc, des-ede3-cbc) : ").lower()
    algo = input("algorithme (RSA, AES-256, 3-DES) : ").upper()
    
    if algo == "RSA":
        cle_priv = input("Clé privée pour le déchiffrement : ")
        if not fichier_existe(cle_priv):
            return console.print("[red]Clé privée introuvable.[/red]")

        cmd = f"openssl pkeyutl -decrypt -in {file_in} -inkey {cle_priv} -out {file_out}"
    #elif algo in ["aes-256-cbc", "des-ede3-cbc"]:
    elif algo in ["AES-256", "3-DES"]:
        if algo == "AES-256":
            cmd = f"openssl enc -d -aes-256-cbc -pbkdf2 -in {file_in} -out {file_out}"
        elif algo == "3-DES":
            cmd = f"openssl enc -d -des-ede3-cbc -pbkdf2 -in {file_in} -out {file_out}"
        #cmd = f"openssl enc -d -{algo} -pbkdf2 -in {file_in} -out {file_out}"
    else:
        console.print("[red]Algorithme non supporté.[/red]")
        return

    executer_commande(cmd)
    console.print("[green]Données déchiffrées avec succès.[/green]")

def cal_em():
    console.print("\n[bold yellow]Calcul d'empreinte[/bold yellow]")
    algo = input("Fonction de hashage (md5, sha256, ...) : ")
    file_in = input("Fichier source : ")
    if not fichier_existe(file_in):
        return console.print("[red]Fichier introuvable.[/red]")
    empreinte = input("Nom du fichier de sortie de l'empreinte : ")

    cmd = f"openssl dgst -{algo} -out {empreinte} {file_in}"
    executer_commande(cmd)
    console.print("[green]Empreinte générée avec succès.[/green]")

def sign_em():
    console.print("\n[bold yellow]Signature d'empreinte[/bold yellow]")
    file_in = input("Fichier à signer : ")
    if not fichier_existe(file_in):
        return console.print("[red]Fichier introuvable.[/red]")
    cle_pri = input("Clé privée : ")
    if not fichier_existe(cle_pri):
        return console.print("[red]Clé privée introuvable.[/red]")
    sig_out = input("Nom du fichier signature : ")

    cmd = f"openssl dgst -sha256 -sign {cle_pri} -out {sig_out} {file_in}"
    executer_commande(cmd)
    console.print("[green]Signature créée avec succès.[/green]")

def ver_sign():
    console.print("\n[bold yellow]Vérification de signature[/bold yellow]")
    file = input("Fichier original (empreinte) : ")
    if not fichier_existe(file):
        return console.print("[red]Fichier original introuvable.[/red]")
    signature = input("Fichier de signature : ")
    if not fichier_existe(signature):
        return console.print("[red]Fichier de signature introuvable.[/red]")
    cle_pub = input("Clé publique : ")
    if not fichier_existe(cle_pub):
        return console.print("[red]Clé publique introuvable.[/red]")

    cmd = f"openssl dgst -sha256 -verify {cle_pub} -signature {signature} {file}"
    executer_commande(cmd)

def main():
    try:
        while True:
            afficher_menu()
            try:
                choice = input("Choisir une option : ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[red]Fermeture de l'application...[/red]")
                break

            match choice:
                case "1": gen_cle_pri()
                case "2": chif_cle()
                case "3": gen_cle_pub()
                case "4": chif_d()
                case "5": dechif_d()
                case "6": cal_em()
                case "7": sign_em()
                case "8": ver_sign()
                case "99": break
                case _: console.print("[red]Option invalide. Veuillez réessayer.[/red]")

    except Exception as e:
        console.print(f"[bold red]Erreur critique : {e}[/bold red]")
    finally:
        console.print("[bold blue]Merci d’avoir utilisé l’outil de cryptographie.[/bold blue]")

if __name__ == "__main__":
    main()
