#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modulo per gestire la configurazione di PyFetch
"""

import os
import sys
import json
import platform

class Config:
    """Classe che gestisce la configurazione di PyFetch."""
    
    def __init__(self, config_path=None):
        """Inizializza la configurazione di PyFetch."""
        # Impostazioni predefinite
        self.settings = {
            # Impostazioni generali
            "show_ascii": True,            # Mostra ASCII art
            "show_colors": True,           # Mostra colori
            "show_color_blocks": True,     # Mostra blocchi di colore
            
            # Selettori di informazioni (quali informazioni mostrare)
            "info": {
                "os": True,
                "kernel": True,
                "uptime": True,
                "packages": True,
                "shell": True,
                "resolution": True,
                "de": True,
                "wm": True,
                "terminal": True,
                "cpu": True,
                "gpu": True,
                "memory": True,
                "disk": True,
                "temperatures": True,
            },
            
            # Impostazioni specifiche per sistema
            "windows_settings": {
                "show_admin": True,        # Mostra se l'utente è amministratore
            },
            "linux_settings": {
                "show_package_managers": [ # Gestori di pacchetti da mostrare
                    "apt", "pacman", "rpm", "flatpak"
                ],
            },
            "darwin_settings": {
                "show_package_managers": [ # Gestori di pacchetti da mostrare
                    "homebrew", "macports"
                ],
            },
            
            # Impostazioni ASCII art
            "ascii_art": {
                "use_custom": False,       # Usa ASCII art personalizzato
                "custom_path": "",         # Percorso all'ASCII art personalizzato
                "distro_override": "",     # Forza l'uso di ASCII art di una distro specifica
            },
        }
        
        # Carica la configurazione se specificata
        if config_path:
            self.load_config(config_path)
        else:
            # Altrimenti cerca nelle posizioni predefinite
            self._try_load_default_config()
            
    def load_config(self, config_path):
        """Carica una configurazione da file."""
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Aggiorna le impostazioni con quelle dell'utente
                self._update_settings(user_config)
        except Exception as e:
            print(f"Attenzione: impossibile caricare il file di configurazione: {e}")
            
    def _try_load_default_config(self):
        """Tenta di caricare la configurazione da percorsi predefiniti."""
        # Determina il sistema operativo
        os_type = platform.system().lower()
        
        # Percorsi di configurazione in base al sistema operativo
        if os_type == "linux" or os_type == "darwin":  # Linux o macOS
            xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
            config_paths = [
                os.path.join(xdg_config, "pyfetch", "config.json"),
                os.path.expanduser("~/.pyfetch.json"),
            ]
        elif os_type == "windows":  # Windows
            app_data = os.environ.get("APPDATA", os.path.expanduser("~/AppData/Roaming"))
            config_paths = [
                os.path.join(app_data, "PyFetch", "config.json"),
                os.path.expanduser("~/pyfetch.json"),
            ]
        else:
            config_paths = [
                os.path.expanduser("~/.pyfetch.json"),
            ]
            
        # Prova a caricare da ogni percorso
        for path in config_paths:
            if os.path.exists(path):
                self.load_config(path)
                break
                
    def _update_settings(self, user_config):
        """Aggiorna le impostazioni con quelle dell'utente."""
        # Funzione ricorsiva per aggiornare dizionari annidati
        def update_dict(target, source):
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    # Se entrambi i valori sono dizionari, aggiorna ricorsivamente
                    update_dict(target[key], value)
                else:
                    # Altrimenti sostituisci il valore
                    target[key] = value
                    
        update_dict(self.settings, user_config)
        
    def get(self, key, default=None):
        """Ottiene un valore di configurazione."""
        # Supporta accesso a chiavi nidificate con notazione a punto (es. "info.cpu")
        keys = key.split(".")
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def save(self, config_path=None):
        """Salva la configurazione corrente su file."""
        if not config_path:
            # Determina il percorso predefinito in base al sistema operativo
            os_type = platform.system().lower()
            
            if os_type == "linux" or os_type == "darwin":  # Linux o macOS
                xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
                config_path = os.path.join(xdg_config, "pyfetch", "config.json")
                
                # Crea la directory se non esiste
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
            elif os_type == "windows":  # Windows
                app_data = os.environ.get("APPDATA", os.path.expanduser("~/AppData/Roaming"))
                config_path = os.path.join(app_data, "PyFetch", "config.json")
                
                # Crea la directory se non esiste
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
            else:
                config_path = os.path.expanduser("~/.pyfetch.json")
                
        try:
            with open(config_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
            print(f"Configurazione salvata in {config_path}")
        except Exception as e:
            print(f"Errore durante il salvataggio della configurazione: {e}")
            
    def create_default_config(self):
        """Crea un file di configurazione predefinito."""
        # Salva la configurazione predefinita
        self.save()