#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyFetch - Un fork di Neofetch scritto in Python
Mostra informazioni di sistema con ASCII art in stile Neofetch
Multipiattaforma: funziona su Windows, Linux e macOS
"""

import os
import sys
import platform
import argparse
from datetime import datetime

# Importa i moduli interni
try:
    from system_info import SystemInfo
    from ascii_art import AsciiArt
    from config import Config
except ImportError:
    print("Errore: Moduli necessari non trovati.")
    print("Assicurati di eseguire lo script dalla directory principale.")
    sys.exit(1)

__version__ = "0.1.0"

def get_available_ascii_art():
    """Restituisce l'elenco di tutte le ASCII art disponibili."""
    # Importa i dizionari delle ASCII art
    try:
        from ascii_art import AsciiArt
        # Unisci i dizionari delle ASCII art
        available_art = list(AsciiArt.ASCII_ART.keys())
        available_distros = list(AsciiArt.LINUX_DISTROS.keys())
        
        # Gestisci i possibili conflitti di nome rimuovendo duplicati
        # o versioni con suffisso _small che potrebbero causare conflitti
        unique_art = set()
        result = []
        
        for art in available_art + available_distros:
            # Verifica se è una versione "_small" che potrebbe creare conflitti
            if "_small" in art and art.replace("_small", "") in available_art:
                continue
                
            # Usa il nome base come chiave per verificare duplicati
            art_base = art.split("_")[0]
            
            # Se il nome base è già stato aggiunto, salta questo elemento
            if art_base in unique_art:
                continue
                
            unique_art.add(art_base)
            result.append(art)
            
        return result
    except ImportError:
        return []

def parse_arguments():
    """Analizza gli argomenti della linea di comando."""
    parser = argparse.ArgumentParser(description="PyFetch - Un fork di Neofetch scritto in Python")
    parser.add_argument("--version", action="version", version=f"PyFetch {__version__}")
    parser.add_argument("--ascii", help="Percorso al file ASCII art personalizzato")
    parser.add_argument("--ascii_distro", help="Specifica la distribuzione ASCII art da utilizzare")
    parser.add_argument("--config", help="Percorso al file di configurazione personalizzato")
    parser.add_argument("--no_color", action="store_true", help="Disabilita i colori")
    
    # Ottieni tutte le ASCII art disponibili
    available_art = get_available_ascii_art()
    
    # Aggiungi un gruppo di argomenti mutuamente esclusivi per le ASCII art
    art_group = parser.add_argument_group('ASCII Art specifiche')
    for art_name in available_art:
        art_group.add_argument(f"--{art_name}", action="store_true", 
                              help=f"Utilizza l'ASCII art di {art_name.capitalize()}")
    
    return parser.parse_args()

def main():
    """Funzione principale."""
    # Analizza gli argomenti
    args = parse_arguments()
    
    # Carica la configurazione
    config = Config(config_path=args.config)
    
    # Inizializza la raccolta informazioni di sistema
    system = SystemInfo(config)
    system_info = system.get_all_info()
    
    # Controlla se è stata specificata una ASCII art tramite flag dedicata
    ascii_distro = args.ascii_distro
    if not ascii_distro:
        # Cerca nelle opzioni se è stata specificata una ASCII art tramite --nome_distro
        available_art = get_available_ascii_art()
        for art_name in available_art:
            if hasattr(args, art_name) and getattr(args, art_name):
                ascii_distro = art_name
                break
    
    # Inizializza l'ASCII art
    ascii_art = AsciiArt(config, 
                         ascii_file=args.ascii, 
                         ascii_distro=ascii_distro, 
                         use_color=not args.no_color)
    
    # Stampa l'ASCII art e le informazioni di sistema
    print("\n")
    ascii_art.print_with_info(system_info)
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperazione interrotta.")
        sys.exit(0)
    except Exception as e:
        print(f"Errore: {e}")
        sys.exit(1)