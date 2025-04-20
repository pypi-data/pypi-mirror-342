# PyFetch

Un fork di Neofetch scritto interamente in Python. Mostra informazioni di sistema con ASCII art in stile Neofetch.

## Caratteristiche

- **Multipiattaforma**: funziona su Windows, Linux e macOS
- **Informazioni complete di sistema**: mostra nome utente, hostname, OS, kernel, uptime, pacchetti, shell, risoluzione, DE/WM, terminale, CPU, GPU, RAM, disco, temperatura
- **ASCII Art**: utilizza le stesse ASCII art di Neofetch, con supporto per art personalizzate
- **Colori ANSI**: supporto completo per terminali a colori
- **Configurabile**: configurazioni personalizzabili tramite file JSON
- **Portatile**: scritto interamente in Python, facilmente estendibile

## Installazione

### Requisiti

- Python 3.6 o superiore
- Modulo `psutil`: `pip install psutil`

### Installazione manuale

```bash
git clone https://github.com/your-username/pyfetch.git
cd pyfetch
pip install -r requirements.txt
```

Alternativamente, puoi installare PyFetch tramite pip:

```bash
pip install pyfetch
```

## Utilizzo

Esegui PyFetch dalla riga di comando:

```bash
python pyfetch.py
```

Oppure, se installato tramite pip:

```bash
pyfetch
```

### Opzioni

- `--ascii FILE`: Utilizza un file ASCII personalizzato
- `--ascii_distro DISTRO`: Utilizza l'ASCII art di una distribuzione specifica
- `--config FILE`: Utilizza un file di configurazione personalizzato
- `--no_color`: Disabilita i colori
- `--version`: Mostra la versione di PyFetch

## Configurazione

PyFetch può essere configurato tramite un file di configurazione JSON. Il file di configurazione predefinito si trova in:

- **Linux/macOS**: `~/.config/pyfetch/config.json` o `~/.pyfetch.json`
- **Windows**: `%APPDATA%\PyFetch\config.json` o `~/pyfetch.json`

### Esempio di configurazione

```json
{
    "show_ascii": true,
    "show_colors": true,
    "show_color_blocks": true,
    "info": {
        "os": true,
        "kernel": true,
        "uptime": true,
        "packages": true,
        "shell": true,
        "resolution": true,
        "de": true,
        "wm": true,
        "terminal": true,
        "cpu": true,
        "gpu": true,
        "memory": true,
        "disk": true,
        "temperatures": true
    },
    "ascii_art": {
        "use_custom": false,
        "custom_path": "",
        "distro_override": ""
    }
}
```

## Estensione

PyFetch è progettato per essere facilmente estendibile. È possibile aggiungere nuove funzionalità modificando i seguenti file:

- `system_info.py`: Aggiungere nuovi metodi per raccogliere informazioni di sistema
- `ascii_art.py`: Aggiungere nuove ASCII art per distribuzioni o sistemi operativi
- `config.py`: Aggiungere nuove opzioni di configurazione

## Contribuire

I contributi sono benvenuti! Se vuoi contribuire a PyFetch, segui questi passaggi:

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/amazing-feature`)
3. Commit delle tue modifiche (`git commit -m 'Aggiunta una nuova feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

## Licenza

Distribuito con licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## Ringraziamenti

- [Neofetch](https://github.com/dylanaraps/neofetch) - L'ispirazione originale per questo progetto