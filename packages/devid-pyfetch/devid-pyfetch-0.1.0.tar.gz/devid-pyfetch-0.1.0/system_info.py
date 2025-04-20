#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modulo per raccogliere tutte le informazioni di sistema
Supporta Windows, Linux e macOS
"""

import os
import sys
import platform
import subprocess
import re
import socket
import time
import psutil
from datetime import datetime, timedelta

# Importazione condizionale di moduli specifici per sistema operativo
if platform.system().lower() == "windows":
    try:
        import wmi  # Questo modulo è necessario solo per Windows
    except ImportError:
        # Il modulo wmi non è installato, ma lo gestiremo più tardi nel codice
        pass

class SystemInfo:
    """Classe che gestisce la raccolta di informazioni di sistema."""
    
    def __init__(self, config):
        """Inizializza la classe SystemInfo."""
        self.config = config
        self.os_type = platform.system().lower()  # windows, linux, darwin
        
    def get_all_info(self):
        """Raccoglie tutte le informazioni di sistema."""
        info = {}
        
        # Informazioni di base sempre disponibili
        info["user"] = self.get_username()
        info["hostname"] = self.get_hostname()
        info["os"] = self.get_os_name()
        info["kernel"] = self.get_kernel_version()
        info["uptime"] = self.get_uptime()
        info["shell"] = self.get_shell()
        info["resolution"] = self.get_screen_resolution()
        info["de"] = self.get_desktop_environment()
        info["wm"] = self.get_window_manager()
        info["terminal"] = self.get_terminal()
        info["cpu"] = self.get_cpu_info()
        info["gpu"] = self.get_gpu_info()
        info["memory"] = self.get_memory_info()
        info["disk"] = self.get_disk_info()
        
        # Informazioni specifiche per OS
        if self.os_type == "linux":
            info["packages"] = self.get_package_count_linux()
        elif self.os_type == "darwin":
            info["packages"] = self.get_package_count_macos()
        elif self.os_type == "windows":
            info["packages"] = self.get_package_count_windows()
        
        # Temperature (se disponibili)
        temps = self.get_temperatures()
        if temps:
            info["temperatures"] = temps
            
        return info
        
    def get_username(self):
        """Restituisce il nome utente."""
        return os.getlogin()
        
    def get_hostname(self):
        """Restituisce il nome host."""
        return socket.gethostname()
        
    def get_os_name(self):
        """Restituisce il nome del sistema operativo."""
        if self.os_type == "windows":
            return platform.system() + " " + platform.release()
        elif self.os_type == "darwin":
            # macOS: ottiene la versione completa
            try:
                mac_ver = platform.mac_ver()[0]
                versions = {
                    "10.15": "Catalina",
                    "11": "Big Sur",
                    "12": "Monterey",
                    "13": "Ventura",
                    "14": "Sonoma"
                }
                major_ver = ".".join(mac_ver.split(".")[:2])
                codename = versions.get(major_ver, "")
                return f"macOS {mac_ver} {codename}".strip()
            except:
                return f"macOS {platform.mac_ver()[0]}"
        else:
            # Linux: cerca di ottenere la distribuzione
            try:
                with open("/etc/os-release") as f:
                    data = {}
                    for line in f:
                        if "=" in line:
                            key, value = line.rstrip().split("=", 1)
                            data[key] = value.strip('"')
                    return f"{data.get('NAME', 'Linux')} {data.get('VERSION', '')}"
            except:
                return platform.system()
    
    def get_kernel_version(self):
        """Restituisce la versione del kernel."""
        return platform.release()
    
    def get_uptime(self):
        """Restituisce il tempo di uptime del sistema."""
        if self.os_type == "windows":
            return str(timedelta(seconds=int(time.time() - psutil.boot_time())))
        else:
            uptime_seconds = int(time.time() - psutil.boot_time())
            days = uptime_seconds // 86400
            hours = (uptime_seconds % 86400) // 3600
            minutes = (uptime_seconds % 3600) // 60
            result = ""
            if days > 0:
                result += f"{days}d "
            if hours > 0 or days > 0:
                result += f"{hours}h "
            result += f"{minutes}m"
            return result
    
    def get_shell(self):
        """Restituisce la shell in uso."""
        if self.os_type == "windows":
            shell = os.environ.get("COMSPEC", "")
            return os.path.basename(shell) if shell else "cmd.exe/PowerShell"
        else:
            shell = os.environ.get("SHELL", "")
            return os.path.basename(shell) if shell else "Unknown"
    
    def get_screen_resolution(self):
        """Restituisce la risoluzione dello schermo."""
        try:
            if self.os_type == "windows":
                from ctypes import windll
                user32 = windll.user32
                width = user32.GetSystemMetrics(0)
                height = user32.GetSystemMetrics(1)
                return f"{width}x{height}"
            elif self.os_type == "darwin":
                cmd = "system_profiler SPDisplaysDataType | grep Resolution"
                result = subprocess.check_output(cmd, shell=True, text=True)
                match = re.search(r"(\d+) x (\d+)", result)
                if match:
                    return f"{match.group(1)}x{match.group(2)}"
            else:  # Linux
                cmd = "xrandr | grep ' connected' | grep -o '[0-9]*x[0-9]*+[0-9]*+[0-9]*'"
                result = subprocess.check_output(cmd, shell=True, text=True)
                return result.strip().split("+")[0]
        except:
            return "Unknown"
    
    def get_desktop_environment(self):
        """Restituisce l'ambiente desktop in uso."""
        if self.os_type == "windows":
            return "Windows Explorer"
        elif self.os_type == "darwin":
            return "Aqua"
        else:
            # Linux
            de = os.environ.get("XDG_CURRENT_DESKTOP", os.environ.get("DESKTOP_SESSION"))
            return de if de else "Unknown"
    
    def get_window_manager(self):
        """Restituisce il window manager in uso."""
        if self.os_type == "windows":
            return "DWM"
        elif self.os_type == "darwin":
            return "Quartz Compositor"
        else:
            try:
                cmd = "wmctrl -m | grep Name:"
                result = subprocess.check_output(cmd, shell=True, text=True)
                return result.split(":")[1].strip()
            except:
                return "Unknown"
    
    def get_terminal(self):
        """Restituisce il terminale in uso."""
        if self.os_type == "windows":
            return os.environ.get("TERM_PROGRAM", "Windows Console/Terminal")
        else:
            return os.environ.get("TERM_PROGRAM", os.environ.get("TERM", "Unknown"))
    
    def get_cpu_info(self):
        """Restituisce informazioni sulla CPU."""
        cpu_info = {}
        cpu_info["model"] = platform.processor()
        cpu_info["cores"] = psutil.cpu_count(logical=False)
        cpu_info["threads"] = psutil.cpu_count(logical=True)
        cpu_info["usage"] = f"{psutil.cpu_percent()}%"
        
        # Se la descrizione della CPU è vuota o contiene informazioni tecniche, prova un metodo alternativo
        if not cpu_info["model"] or cpu_info["model"] == "" or "family" in cpu_info["model"].lower() or "intel64" in cpu_info["model"].lower():
            if self.os_type == "windows":
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                         r"HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0")
                    cpu_info["model"] = winreg.QueryValueEx(key, "ProcessorNameString")[0]
                    winreg.CloseKey(key)
                    
                    # Pulizia del nome della CPU
                    model = cpu_info["model"]
                    
                    # Rimuovi prefissi e suffissi comuni
                    model = re.sub(r"Intel\(R\) Core\(TM\)", "Intel", model)
                    model = re.sub(r"AMD", "AMD", model)
                    model = re.sub(r"Processor", "", model)
                    model = re.sub(r"CPU", "", model)
                    model = re.sub(r"\s+@\s+.*$", "", model)  # Rimuovi la parte con la frequenza
                    model = re.sub(r"\s+GHz$", "", model)  # Rimuovi la parte con GHz
                    model = re.sub(r"\s+MHz$", "", model)  # Rimuovi la parte con MHz
                    
                    # Rimuovi spazi multipli
                    model = re.sub(r"\s+", " ", model).strip()
                    
                    cpu_info["model"] = model
                except:
                    pass
            elif self.os_type == "linux":
                try:
                    with open("/proc/cpuinfo") as f:
                        for line in f:
                            if "model name" in line:
                                model = line.split(":")[1].strip()
                                # Pulizia del nome della CPU
                                model = re.sub(r"Intel\(R\) Core\(TM\)", "Intel", model)
                                model = re.sub(r"AMD", "AMD", model)
                                model = re.sub(r"Processor", "", model)
                                model = re.sub(r"CPU", "", model)
                                model = re.sub(r"\s+@\s+.*$", "", model)
                                model = re.sub(r"\s+GHz$", "", model)
                                model = re.sub(r"\s+MHz$", "", model)
                                model = re.sub(r"\s+", " ", model).strip()
                                cpu_info["model"] = model
                                break
                except:
                    pass
            elif self.os_type == "darwin":
                try:
                    cmd = "sysctl -n machdep.cpu.brand_string"
                    model = subprocess.check_output(cmd, shell=True, text=True).strip()
                    # Pulizia del nome della CPU
                    model = re.sub(r"Intel\(R\) Core\(TM\)", "Intel", model)
                    model = re.sub(r"AMD", "AMD", model)
                    model = re.sub(r"Processor", "", model)
                    model = re.sub(r"CPU", "", model)
                    model = re.sub(r"\s+@\s+.*$", "", model)
                    model = re.sub(r"\s+GHz$", "", model)
                    model = re.sub(r"\s+MHz$", "", model)
                    model = re.sub(r"\s+", " ", model).strip()
                    cpu_info["model"] = model
                except:
                    pass
                    
        # Se dopo tutti i tentativi abbiamo ancora un nome troppo lungo o tecnico, proviamo a estrarne la parte più significativa
        if len(cpu_info["model"]) > 50 or "family" in cpu_info["model"].lower():
            # Cerca di estrarre un pattern come "i7-12700H" o "Ryzen 9 5900X"
            intel_match = re.search(r"i[3579]-\d{4,5}[A-Z]*", cpu_info["model"])
            amd_match = re.search(r"Ryzen\s+\d+\s+\d{4}[A-Z]*", cpu_info["model"])
            
            if intel_match:
                cpu_info["model"] = f"Intel {intel_match.group(0)}"
            elif amd_match:
                cpu_info["model"] = f"AMD {amd_match.group(0)}"
                
        return cpu_info
    
    def get_gpu_info(self):
        """Restituisce informazioni sulla GPU."""
        gpu_info = {"model": "Unknown"}
        
        try:
            if self.os_type == "windows":
                # Metodo 1: Utilizzo del modulo WMI se disponibile
                wmi_available = False
                try:
                    if 'wmi' in sys.modules:
                        import wmi
                        wmi_available = True
                except (ImportError, AttributeError):
                    wmi_available = False
                
                if wmi_available:
                    try:
                        w = wmi.WMI()
                        gpu_info["model"] = w.Win32_VideoController()[0].Name
                    except Exception as e:
                        # Se qualcosa va storto con WMI, passa al metodo PowerShell
                        pass
                
                # Metodo 2: Fallback usando PowerShell (se WMI non è disponibile o fallisce)
                if gpu_info["model"] == "Unknown":
                    cmd = "powershell \"Get-WmiObject Win32_VideoController | Select-Object -ExpandProperty Name\""
                    result = subprocess.check_output(cmd, shell=True, text=True)
                    if result:
                        gpu_info["model"] = result.strip()
            elif self.os_type == "linux":
                cmd = "lspci | grep -i 'vga\\|3d\\|2d'"
                result = subprocess.check_output(cmd, shell=True, text=True)
                if result:
                    match = re.search(r"VGA compatible controller: (.*)", result)
                    if match:
                        gpu_info["model"] = match.group(1).strip()
            elif self.os_type == "darwin":
                cmd = "system_profiler SPDisplaysDataType | grep Chipset"
                result = subprocess.check_output(cmd, shell=True, text=True)
                if result:
                    gpu_info["model"] = result.split(":")[1].strip()
        except Exception as e:
            # Registra l'errore ma continua con il valore predefinito
            gpu_info["model"] = f"Unknown (Error: {str(e)[:50]}...)" if len(str(e)) > 50 else f"Unknown (Error: {e})"
            
        return gpu_info
    
    def get_memory_info(self):
        """Restituisce informazioni sulla memoria."""
        mem = psutil.virtual_memory()
        
        # Conversione in GiB
        total_gb = mem.total / (1024 ** 3)
        used_gb = (mem.total - mem.available) / (1024 ** 3)
        
        return {
            "total": f"{total_gb:.1f} GiB",
            "used": f"{used_gb:.1f} GiB",
            "percent": f"{mem.percent}%"
        }
    
    def get_disk_info(self):
        """Restituisce informazioni sul disco."""
        disk = {}
        try:
            disk_usage = psutil.disk_usage('/')
            total_gb = disk_usage.total / (1024 ** 3)
            used_gb = disk_usage.used / (1024 ** 3)
            disk = {
                "total": f"{total_gb:.1f} GiB",
                "used": f"{used_gb:.1f} GiB",
                "percent": f"{disk_usage.percent}%"
            }
        except:
            disk = {"error": "Impossibile ottenere informazioni sul disco"}
            
        return disk
    
    def get_package_count_linux(self):
        """Restituisce il conteggio dei pacchetti installati su Linux."""
        packages = {}
        
        package_managers = {
            "apt": "dpkg -l | grep -c '^ii'",
            "pacman": "pacman -Q | wc -l",
            "rpm": "rpm -qa | wc -l",
            "portage": "ls -d /var/db/pkg/*/* | wc -l",
            "flatpak": "flatpak list | wc -l"
        }
        
        for manager, command in package_managers.items():
            try:
                count = subprocess.check_output(command, shell=True, text=True).strip()
                if int(count) > 0:
                    packages[manager] = count
            except:
                continue
                
        return packages
    
    def get_package_count_macos(self):
        """Restituisce il conteggio dei pacchetti installati su macOS."""
        packages = {}
        
        package_managers = {
            "homebrew": "brew list --formula | wc -l",
            "homebrew-cask": "brew list --cask | wc -l",
            "macports": "port installed | wc -l"
        }
        
        for manager, command in package_managers.items():
            try:
                count = subprocess.check_output(command, shell=True, text=True).strip()
                if int(count) > 0:
                    packages[manager] = count
            except:
                continue
                
        return packages
    
    def get_package_count_windows(self):
        """Restituisce il conteggio dei pacchetti installati su Windows."""
        packages = {}
        
        # Conta programmi installati
        try:
            # Approccio alternativo che usa REG QUERY al posto di PowerShell
            cmd = "reg query HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall /s /v DisplayName | find /c \"DisplayName\""
            count = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
            packages["Programs"] = count
        except:
            try:
                # Fallback originale usando PowerShell se possibile
                cmd = "powershell \"Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Measure-Object | Select-Object -ExpandProperty Count\""
                count = subprocess.check_output(cmd, shell=True, text=True).strip()
                packages["Programs"] = count
            except:
                # Ultimo tentativo - valore fisso
                packages["Programs"] = "N/A"
            
        # Conta pacchetti winget se disponibile
        try:
            # Prima controlla se winget esiste
            check_winget = "where winget"
            subprocess.check_output(check_winget, shell=True, text=True, stderr=subprocess.DEVNULL)
            
            # Winget esiste, prova a contare i pacchetti
            cmd = "winget list | find /c \"Name\""
            count = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
            # Sottrai 2 per l'intestazione e la riga vuota
            count = max(0, int(count) - 2)
            if count > 0:
                packages["winget"] = str(count)
        except:
            # Winget non disponibile o errore, ignora silenziosamente
            pass
            
        # Conta pacchetti Chocolatey se disponibile
        try:
            # Prima controlla se choco esiste
            check_choco = "where choco"
            subprocess.check_output(check_choco, shell=True, text=True, stderr=subprocess.DEVNULL)
            
            # Chocolatey esiste, prova a contare i pacchetti
            cmd = "choco list --local-only | find /c \"packages installed\""
            count = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
            if int(count) > 0:
                packages["chocolatey"] = count
        except:
            # Chocolatey non disponibile o errore, ignora silenziosamente
            pass
            
        return packages
    
    def get_temperatures(self):
        """Restituisce le temperature del sistema se disponibili."""
        temps = {}
        
        try:
            temps_data = psutil.sensors_temperatures()
            for chip, sensors in temps_data.items():
                for sensor in sensors:
                    if sensor.current and sensor.label:
                        temps[f"{chip}_{sensor.label}"] = f"{sensor.current}°C"
                    elif sensor.current:
                        temps[chip] = f"{sensor.current}°C"
        except:
            return None
            
        return temps if temps else None