#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modulo per gestire le ASCII art per PyFetch
Mantiene lo stile originale di Neofetch
"""

import os
import platform
import re
import random

class AsciiArt:
    """Classe che gestisce l'ASCII art e la visualizzazione."""
    
    # Colori ANSI
    COLORS = {
        "reset": "\033[0m",
        "black": "\033[0;30m",
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "yellow": "\033[0;33m",
        "blue": "\033[0;34m",
        "magenta": "\033[0;35m",
        "cyan": "\033[0;36m",
        "white": "\033[0;37m",
        "bold_black": "\033[1;30m",
        "bold_red": "\033[1;31m",
        "bold_green": "\033[1;32m",
        "bold_yellow": "\033[1;33m",
        "bold_blue": "\033[1;34m",
        "bold_magenta": "\033[1;35m",
        "bold_cyan": "\033[1;36m",
        "bold_white": "\033[1;37m",
    }
    
    # Mapping del colore predefinito per sistema operativo
    DEFAULT_COLORS = {
        "windows": "cyan",
        "linux": "yellow",
        "darwin": "white",
        "android": "green",  # Aggiungi colore per Android
        "aix": "green",
        "instantos": "blue", 
        "artix": "cyan",
        "arch": "cyan",
        "archcraft": "cyan",
        "archlabs": "cyan",
        "archstrike": "cyan",
        "alpine": "blue",
        "almalinux": "red",
        "alter": "cyan",
        "amazon": "yellow",
        "anarchy": "white",
        "antergos": "blue",
        "antix": "red",
        "aosc": "blue",
        "apricity": "blue",
        "archbox": "green",
        "archmerge": "cyan",
        "hash": "cyan",
        "aperio": "white",
        "manjaro": "green",
        "fedora": "blue",
        "kubuntu": "blue",
        "ubuntu": "red",
        "i3buntu": "red",
        "linuxmint": "green",
        "mint": "green", 
        "nixos": "blue",
        "popos": "cyan",
        "pop_os": "cyan",
    }
    
    # ASCII art predefinite
    ASCII_ART = {
        "windows": [
            "                                  ..,",
            "                      ....,,:;+ccllll",
            "        ...,,+:;  cllllllllllllllllll",
            "  ,cclllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "                                     ",
            "  llllllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "  llllllllllllll  lllllllllllllllllll",
            "  `'ccllllllllll  lllllllllllllllllll",
            "        `' \\*::  :ccllllllllllllllll",
            "                      ````''*::cll",
            "                                 ``",
        ],
        "linux": [
            "            .-\"\"\"-.           ",
            "           '       \\          ",
            "          |,.  ,-.  |         ",
            "          |()L( ()| |         ",
            "          |,'  `\".| |         ",
            "          |.___.',| `         ",
            "         .j `--\"' `  `.       ",
            "        / '        '   \\      ",
            "       / /          `   `.    ",
            "      / /            `    .   ",
            "     / /              l   |   ",
            "    . ,               |   |   ",
            "    ,\"`\\             .|   |   ",
            " _.'   ``.          | `..-'l  ",
            "|       `.`,        |      `. ",
            "|         `.    __.j         )",
            "|__        |--\"\"___|      ,-'",
            "   `\"--...,+\"\"\"\"   `._,.-'   ",
        ],
        "darwin": [
            "                    c.'",
            "                 ,xNMM.",
            "               .OMMMMo",
            "               lMMM0,",
            "     .;loddo:.  .olloddol;.",
            "   cKMMMMMMMMMMNWMMMMMMMMMM0:",
            " .KMMMMMMMMMMMMMMMMMMMMMMMWd.",
            " XMMMMMMMMMMMMMMMMMMMMMMMX.",
            ";MMMMMMMMMMMMMMMMMMMMMMMM:",
            ":MMMMMMMMMMMMMMMMMMMMMMMM:",
            ".MMMMMMMMMMMMMMMMMMMMMMMMX.",
            " kMMMMMMMMMMMMMMMMMMMMMMMMWd.",
            " .XMMMMMMMMMMMMMMMMMMMMMMMMMMk",
            "  .XMMMMMMMMMMMMMMMMMMMMMMMMK.",
            "    kMMMMMMMMMMMMMMMMMMMMMMd",
            "     ;KMMMMMMMWXXWMMMMMMMk.",
            "       .cooc,.    .,coo:.",
        ],
        "android": [
            "         -o          o-       ",
            "          +hydNNNNdyh+        ",
            "        +mMMMMMMMMMMMMm+      ",
            "      `dMMm:NMMMMMMN:mMMd`    ",
            "      hMMMMMMMMMMMMMMMMMMh    ",
            "  ..  yyyyyyyyyyyyyyyyyyyy  ..",
            ".mMMm`MMMMMMMMMMMMMMMMMMMM`mMMm.",
            ":MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM:",
            ":MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM:",
            ":MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM:",
            ":MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM:",
            "-MMMM-MMMMMMMMMMMMMMMMMMMM-MMMM-",
            " +yy+ MMMMMMMMMMMMMMMMMMMM +yy+ ",
            "      mMMMMMMMMMMMMMMMMMMm       ",
            "      `/++MMMMh++hMMMM++/`     ",
            "          MMMMo  oMMMM         ",
            "          MMMMo  oMMMM         ",
            "          oNMm-  -mMNs         ",
        ],
        "generic": [
            "        .-.        ",
            "       /'v'\\       ",
            "      (/   \\)      ",
            "     =======      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            "     |     |      ",
            " jgs '-----'      ",
        ],
        "android_small": [
            "  ;,           ,;",
            "   ';,.-----.,;'",
            "  ,'           ',",
            " /    O     O    \\",
            "|                 |",
            "'-----------------'",
        ],
        "aix": [
            "           `:+ssssossossss+-`",
            "        .oys///oyhddddhyo///sy+.",
            "      /yo:+hNNNNNNNNNNNNNNNNh+:oy/",
            "    :h/:yNNNNNNNNNNNNNNNNNNNNNNy-+h:",
            "  `ys.yNNNNNNNNNNNNNNNNNNNNNNNNNNy.ys",
            " `h+-mNNNNNNNNNNNNNNNNNNNNNNNNNNNNm-oh",
            " h+-NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN.oy",
            "/d`mNNNNNNN/::mNNNd::m+:/dNNNo::dNNNd`m:",
            "h//NNNNNNN: . .NNNh  mNo  od. -dNNNNN:+y",
            "N.sNNNNNN+ -N/ -NNh  mNNd.   sNNNNNNNo-m",
            "N.sNNNNNs  +oo  /Nh  mNNs` ` /mNNNNNNo-m",
            "h//NNNNh  ossss` +h  md- .hm/ `sNNNNN:+y",
            ":d`mNNN+/yNNNNNd//y//h//oNNNNy//sNNNd`m-",
            " yo-NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNm.ss",
            " `h+-mNNNNNNNNNNNNNNNNNNNNNNNNNNNNm-oy",
            "   sy.yNNNNNNNNNNNNNNNNNNNNNNNNNNs.yo",
            "    :h+-yNNNNNNNNNNNNNNNNNNNNNNs-oh-",
            "      :ys:/yNNNNNNNNNNNNNNNmy/:sy:",
            "        .+ys///osyhhhhys+///sy+.",
            "            -/osssossossso/-",
        ],
        "aperio": [
            "",
            " _.._  _ ._.. _",
            "(_][_)(/,[  |(_)",
            "   |   GNU/Linux",
        ],
        "hash": [
            "",
            "      +   ######   +",
            "    ###   ######   ###",
            "  #####   ######   #####",
            " ######   ######   ######",
            "",
            "####### '\"###### '\"########",
            "#######   ######   ########",
            "#######   ######   ########",
            "",
            " ###### '\"###### '\"######",
            "  #####   ######   #####",
            "    ###   ######   ###",
            "      ~   ######   ~",
            "",
        ],
        "almalinux": [
            "         'c:.",
            "        lkkkx, ..       ..   ,cc,",
            "        okkkk:ckkx'  .lxkkx.okkkkd",
            "        .:llcokkx'  :kkkxkko:xkkd,",
            "      .xkkkkdood:  ;kx,  .lkxlll;",
            "       xkkx.       xk'     xkkkkk:",
            "       'xkx.       xd      .....,..",
            "      .. :xkl'     :c      ..''....",
            "    .dkx'  .:ldl:'. '  ':lollldkkxo;",
            "  .''lkkko'                     ckkkx.",
            "'xkkkd:kkd.       ..  ;'        :kkxo.",
            ",xkkkd;kk'      ,d;    ld.   ':dkd::cc,",
            " .,,.;xkko'.';lxo.      dx,  :kkk'xkkkkc",
            "     'dkkkkkxo:.        ;kx  .kkk:;xkkd.",
            "       .....   .;dk:.   lkk.  :;,",
            "             :kkkkkkkdoxkkx",
            "              ,c,,;;;:xkkd.",
            "                ;kkkkl...",
            "                ;kkkkl",
            "                 ,od;",
        ],
        "alpine_small": [
            "   /\\ /\\",
            "  // \\  \\",
            " //   \\  \\",
            "//    \\  \\",
            "//      \\  \\",
            "         \\",
        ],
        "alpine": [
            "       .hddddddddddddddddddddddh.",
            "      :dddddddddddddddddddddddddd:",
            "     /dddddddddddddddddddddddddddd/",
            "    +dddddddddddddddddddddddddddddd+",
            "  `sdddddddddddddddddddddddddddddddds`",
            " `ydddddddddddd++hdddddddddddddddddddy`",
            ".hddddddddddd+`  `+ddddh:-sdddddddddddh.",
            "hdddddddddd+`      `+y:    .sddddddddddh",
            "ddddddddh+`   `//`   `.`     -sddddddddd",
            "ddddddh+`   `/hddh/`   `:s-    -sddddddd",
            "ddddh+`   `/+/dddddh/`   `+s-    -sddddd",
            "ddd+`   `/o` :dddddddh/`   `oy-    .yddd",
            "hdddyo+ohddyosdddddddddho+oydddy++ohdddh",
            ".hddddddddddddddddddddddddddddddddddddh.",
            " `yddddddddddddddddddddddddddddddddddy`",
            "  `sdddddddddddddddddddddddddddddddds`",
            "    +dddddddddddddddddddddddddddddd+",
            "     /dddddddddddddddddddddddddddd/",
            "      :dddddddddddddddddddddddddd:",
            "       .hddddddddddddddddddddddh.",
        ],
        "alter": [
            "                      %,",
            "                    ^WWWw",
            "                   'wwwwww",
            "                  !wwwwwwww",
            "                 #`wwwwwwwww",
            "                @wwwwwwwwwwww",
            "               wwwwwwwwwwwwwww",
            "              wwwwwwwwwwwwwwwww",
            "             wwwwwwwwwwwwwwwwwww",
            "            wwwwwwwwwwwwwwwwwwww,",
            "           w~1i.wwwwwwwwwwwwwwwww,",
            "         3~:~1lli.wwwwwwwwwwwwwwww.",
            "        :~~:~?ttttzwwwwwwwwwwwwwwww",
            "       #<~:~~~~?llllltO-.wwwwwwwwwww",
            "      #~:~~:~:~~?ltlltlttO-.wwwwwwwww",
            "     @~:~~: ~:~~:~:(zttlltltlOda.wwwwwww",
            "    @~:~~: ~:~~:~:(zltlltlO    a,wwwwww",
            "   8~~:~~:~~~~:~~~~_1ltltu          ,www",
            "  5~~:~~:~~:~~:~~:~~~_1ltq             N,,",
            " g~:~~:~~~:~~:~~:~:~~~~1q                N,",
        ],
        "amazon": [
            "             `-/oydNNdyo:.`",
            "      `.:+shmMMMMMMMMMMMMMMmhs+:.`",
            "    -+hNNMMMMMMMMMMMMMMMMMMMMMMNNho-",
            ".``      -/+shmNNMMMMMMNNmhs+/-      ``.",
            "dNmhs+:.       `.:/oo/:.`       .:+shmNd",
            "dMMMMMMMNdhs+:..        ..:+shdNMMMMMMMd",
            "dMMMMMMMMMMMMMMNds    odNMMMMMMMMMMMMMMd",
            "dMMMMMMMMMMMMMMMMh    yMMMMMMMMMMMMMMMMd",
            "dMMMMMMMMMMMMMMMMh    yMMMMMMMMMMMMMMMMd",
            "dMMMMMMMMMMMMMMMMh    yMMMMMMMMMMMMMMMMd",
            "dMMMMMMMMMMMMMMMMh    yMMMMMMMMMMMMMMMMd",
            "dMMMMMMMMMMMMMMMMh    yMMMMMMMMMMMMMMMMd",
            "dMMMMMMMMMMMMMMMMh    yMMMMMMMMMMMMMMMMd",
            "dMMMMMMMMMMMMMMMMh    yMMMMMMMMMMMMMMMMd",
            ".:+ydNMMMMMMMMMMMh    yMMMMMMMMMMMNdy+:.",
            "     `.:+shNMMMMMh    yMMMMMNhs+:``",
            "            `-+shy    shs+:`",
        ],
        "anarchy": [
            "                         ...",
            "                        ....",
            "                      :....",
            "                    :++++.",
            "              .:::++++++++::.",
            "          .:+######++++++######+:.",
            "       .+#########+++++##########:.",
            "     .+##########+++++++++###########+.",
            "    +###########+++++++++############:",
            "   +##########++++++#+++++############+",
            "  +###########+++++###+++++############+",
            " :##########+#+++++####+++++############:",
            " ###########+++++#####+++++##+###++######+",
            ".##########++++++#####++++++++++++#######.",
            ".##########++++++++++++++++++###########.",
            " #####+++++++++++++++###++++++++#########+",
            " :###+++++++++++#########++++++++#########:",
            "  +######+++++##########+++++++++#######+",
            "   +####+++++###########+++++++++#####+",
            "    :##++++++############+++++++++##:",
            "     .++++++#############+++++++++.",
            "      :++++###############+++++::",
            "     .++. .:+##############++++++..",
            "     .:.      ..::++++++::...:++++.",
            "     .                       .:+++.",
            "                                .::",
            "                                   ..",
            "                                    ..",
            "                                    ..",
        ],
        "antergos": [
            "              `.-/ossyyyysso/:.",
            "         .:oyyyyyyyyyyyyyyyyyyo:`",
            "      -oyyyyyyydMMyyyyyyyysyyyyo-",
            "    -syyyyyyyyydMMoyyyyyydMMyyyyyys-",
            "   oyyyysdMyyyyydMMMMMMMMMMMMyyyyyyo",
            " `oyyyyydMMMMyyyysoooooodMMMMyyyyyyo`",
            " oyyyyyydMMMMyyyyyyyyyyyysdMMyssssyyyo",
            "-yyyyyyyyyydMyyyyyyyyyyyyyysdMMMMMysyyy-",
            "oyyyysoodMyyyyyyyyyyyyyyyyyyyydMMMMysyyyo",
            "yyyydMMMMMyyyyyyyyyyyyyyyyyyysosyyyyyyyy",
            "yyyydMMMMMyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "oyyyyysosdyyyyyyyyyyyyyyyyyyydMMMMysyyyo",
            "-yyyyyyyyyydMyyyyyyyyyyyyyysdMMMMMysyyy-",
            " oyyyyyydMMMyyyyyyyyyyyyyysdMMoyyyoyyyo",
            " `oyyyyydMMMyyyyyoooooodMMMMyyyyyyyo",
            "   oyyysyyoyyyysdMMMMMMMMMMyyyyyyyyo",
            "    -syyyyyyyyydMMMysyyydMMMyyyyyys-",
            "      -oyyyyyyyydMMyyyyyyysosyyyyo-",
            "        ./oyyyyyyyyyyyyyyyyyyo/.",
            "           `.:/oosyyyysso/:.`",
        ],
        "antix": [
            "",
            "                    \\",
            "         , - ~ ^ ~ - \\        /",
            "     , '              \\ ' ,  /",
            "   ,                   \\   '/",
            "  ,                     \\  / ,",
            " ,___,                   \\/   ,",
            " /   |   _  _  _|_ o     /\\   ,",
            "|,   |  / |/ |  |  |    /  \\  ,",
            " \\,_/\\_/  |  |_/|_/|_/_/    \\,",
            "   ,                  /     ,\\",
            "     ,               /  , '   \\",
            "      ' - , _ _ _ ,  '",
        ],
        "aosc": [
            "             .:+syhhhhys+:.",
            "         .ohNMMMMMMMMMMMMMMNho.",
            "      `+mMMMMMMMMMMmdmNMMMMMMMMm+`",
            "     +NMMMMMMMMMMMM/   `./smMMMMMN+",
            "   .mMMMMMMMMMMMMMMo        -yMMMMMm.",
            "  :NMMMMMMMMMMMMMMMs          .hMMMMN:",
            " .NMMMMhmMMMMMMMMMMm+/-         oMMMMN.",
            " dMMMMs  ./ymMMMMMMMMMMNy.       sMMMMd",
            "-MMMMN`      oMMMMMMMMMMMN:      `NMMMM-",
            "/MMMMh       NMMMMMMMMMMMMm       hMMMM/",
            "/MMMMh       NMMMMMMMMMMMMm       hMMMM/",
            "-MMMMN`      :MMMMMMMMMMMMy.     `NMMMM-",
            " dMMMMs       .yNMMMMMMMMMMMNy/. sMMMMd",
            " .NMMMMo         -/+sMMMMMMMMMMMmMMMMN.",
            "  :NMMMMh.          .MMMMMMMMMMMMMMMN:",
            "   .mMMMMMy-         NMMMMMMMMMMMMMm.",
            "     +NMMMMMms/.`    mMMMMMMMMMMMN+",
            "      `+mMMMMMMMMNmddMMMMMMMMMMm+`",
            "         .ohNMMMMMMMMMMMMMMNho.",
            "             .:+syhhhhys+:.",
        ],
        "apricity": [
            "                                    ./o-",
            "          ``...``              `:. -/::",
            "     `-+ymNMMMMMNmho-`      :sdNNm/",
            "   `+dMMMMMMMMMMMMMMMmo` sh:.:::-",
            "  /mMMMMMMMMMMMMMMMMMMMm/`sNd/",
            " oMMMMMMMMMMMMMMMMMMMMMMMs -`",
            ":MMMMMMMMMMMMMMMMMMMMMMMMM/",
            "NMMMMMMMMMMMMMMMMMMMMMMMMMd",
            "MMMMMMMmdmMMMMMMMMMMMMMMMMd",
            "MMMMMMy` .mMMMMMMMMMMMmho:`",
            "MMMMMMNo/sMMMMMMMNdy+-.`-/",
            "MMMMMMMMMMMMNdy+:.`.:ohmm:",
            "MMMMMMMmhs+-.`.:+ymNMMMy.",
            "MMMMMM/`.-/ohmNMMMMMMy-",
            "MMMMMMNmNNMMMMMMMMmo.",
            "MMMMMMMMMMMMMMMms:`",
            "MMMMMMMMMMNds/.",
            "dhhyys+/-`",
        ],
        "archcraft": [
            "                   -m:",
            "                  :NMM+      .+",
            "                 +MMMMMo    -NMy",
            "                sMMMMMMMy  -MMMMh`",
            "               yMMMMMMMMMd` oMMMMd`",
            "             `dMMMMMMMMMMMm. /MMMMm-",
            "            .mMMMMMm-dMMMMMN- :NMMMN:",
            "           -NMMMMMd`  yMMMMMN: .mMMMM/",
            "          :NMMMMMy     sMMMMMM+ `dMMMMo",
            "         +MMMMMMs       +MMMMMMs `hMMMMy",
            "        oMMMMMMMds-      :NMMMMMy  sMMMMh`",
            "       yMMMMMNoydMMmo`    -NMMMMMd` +MMMMd.",
            "     `dMMMMMN-   `:yNNs`   .mMMMMMm. /MMMMm-",
            "    .mMMMMMm.        :hN/   `dMMMMMN- -NMMMN:",
            "   -NMMMMMd`           -hh`  `yMMMMMN: .mMMMM/",
            "  :NMMMMMy         `s`   :h.   oMMMMMM+ `-----",
            " +MMMMMMo         .dMm.   `o.   +MMMMMMo",
            "sMMMMMM+         .mMMMN:    :`   :NMMMMMy",
        ],
        "archbox": [
            "              ...:+oh/:::..         ",
            "         ..-/oshhhhhh`   `::::-.",
            "     .:/ohhhhhhhhhhhh`        `-::::.  ",
            " .+shhhhhhhhhhhhhhhhh`             `.::-.  ",
            " /`-:+shhhhhhhhhhhhhh`            .-/+shh  ",
            " /      .:/ohhhhhhhhh`       .:/ohhhhhhhh  ",
            " /           `-:+shhh`  ..:+shhhhhhhhhhhh  ",
            " /                 .:ohhhhhhhhhhhhhhhhhhh  ",
            " /                  `hhhhhhhhhhhhhhhhhhhh  ",
            " /                  `hhhhhhhhhhhhhhhhhhhh  ",
            " /                  `hhhhhhhhhhhhhhhhhhhh  ",
            " /                  `hhhhhhhhhhhhhhhhhhhh  ",
            " /      .+o+        `hhhhhhhhhhhhhhhhhhhh  ",
            " /     -hhhhh       `hhhhhhhhhhhhhhhhhhhh  ",
            " /     ohhhhho      `hhhhhhhhhhhhhhhhhhhh  ",
            " /:::+`hhhhoos`     `hhhhhhhhhhhhhhhhhs+`  ",
            "    `--/:`   /:     `hhhhhhhhhhhho/-    ",
            "             -/:.   `hhhhhhs+:-`    ",
            "                ::::/ho/-`     ",
        ],
        "archlabs": [
            "                     'c'",
            "                    'kKk,",
            "                   .dKKKx.",
            "                  .oKXKXKd.",
            "                 .l0XXXXKKo.",
            "                 c0KXXXXKX0l.",
            "                :0XKKOxxOKX0l.",
            "               :OXKOc. .c0XX0l.",
            "              :OK0o. ....'dKKX0l.",
            "             :OX0c  ;xOx''dKXX0l.",
            "            :0KKo..o0XXKd'.lKXX0l.",
            "           c0XKd..oKXXXXKd..oKKX0l.",
            "         .c0XKk;.l0K0OO0XKd..oKXXKo.",
            "        .l0XXXk:,dKx,.'l0XKo..kXXXKo.",
            "       .o0XXXX0d,:x;   .oKKx'.dXKXXKd.",
            "      .oKXXXXKK0c.;.    :00c'cOXXXXXKd.",
            "     .dKXXXXXXXXk,.     cKx''xKXXXXXXKx'",
            "    'xKXXXXK0kdl:.     .ok; .cdk0KKXXXKx'",
            "   'xKK0koc,..         'c,     ..,cok0KKk,",
            "  ,xko:'.             ..            .':okx;",
            " .,'.                                   .',.  ",
        ],
        "archmerge": [
            "                    y:",
            "                  sMN-",
            "                 +MMMm`",
            "                /MMMMMd`",
            "               :NMMMMMMy",
            "              -NMMMMMMMMs",
            "             .NMMMMMMMMMM+",
            "            .mMMMMMMMMMMMM+",
            "            oNMMMMMMMMMMMMM+",
            "          `+:-+NMMMMMMMMMMMM+",
            "          .sNMNhNMMMMMMMMMMMM/",
            "        `hho/sNMMMMMMMMMMMMMMM/",
            "       `.`omMMmMMMMMMMMMMMMMMMM+",
            "      .mMNdshMMMMd+::oNMMMMMMMMMo",
            "     .mMMMMMMMMM+     `yMMMMMMMMMs",
            "    .NMMMMMMMMM/        yMMMMMMMMMy",
            "   -NMMMMMMMMMh         `mNMMMMMMMMd`",
            "  /NMMMNds+:.`             `-/oymMMMm.",
            " +Mmy/.                          `:smN:",
            "/+.                                  -o.",
        ],
        "arch_small": [
            "      /\\",
            "     /  \\",
            "    /\\   \\",
            "   /      \\",
            "  /   ,,   \\",
            " /   |  |  -\\",
            "/_-''    ''-_\\",
        ],
        "arch": [
            "                   -`",
            "                  .o+`",
            "                 `ooo/",
            "                `+oooo:",
            "               `+oooooo:",
            "               -+oooooo+:",
            "             `/:-:++oooo+:",
            "            `/++++/+++++++:",
            "           `/++++++++++++++:",
            "          `/+++ooooooooooooo/`",
            "         ./ooosssso++osssssso+`",
            "        .oossssso-````/ossssss+`",
            "       -osssssso.      :ssssssso.",
            "      :osssssss/        osssso+++.",
            "     /ossssssss/        +ssssooo/-",
            "   `/ossssso+/:-        -:/+osssso+-",
            "  `+sso+:-`                 `.-/+oso:",
            " `++:.                           `-/+/",
            " .`                                 `/",
        ],
        "archstrike": [
            "                   *   ",
            "                  **.",
            "                 ****",
            "                ******",
            "                *******",
            "              ** *******",
            "             **** *******",
            "            ****_____***/",
            "           ***/*******//***",
            "          **//*******///*/*",
            "         **//*******////*/*",
            "        **//*****//////.,****/*/*",
            "       ***/*****/////////**/*",
            "      ****/****    /////***/*",
            "     ******/***  ////   **/*",
            "    ********/* ///      */********",
            "  ,******     // ______ /    ******,",
        ],
        "artix_small": [
            "      /\\",
            "     /  \\",
            "    /`'.,\\",
            "   /     ',",
            "  /      ,`\\",
            " /   ,.'`.  \\",
            "/.,'`     `'.\\",
        ],
        "artix": [
            "                   '",
            "                  'o'",
            "                 'ooo'",
            "                'ooxoo'",
            "               'ooxxxoo'",
            "              'oookkxxoo'",
            "             'oiioxkkxxoo'",
            "            ':;:iiiioxxxoo'",
            "               `'.;::ioxxoo'",
            "          '-.      `':;jiooo'",
            "         'oooio-..     `'i:io'",
            "        'ooooxxxxoio:,.   `'-;'",
            "       'ooooxxxxxkkxoooIi:-.  `'",
            "      'ooooxxxxxkkkkxoiiiiiji'",
            "     'ooooxxxxxkxxoiiii:'`     .i'",
            "    'ooooxxxxxoi:::'`       .;ioxo'",
            "   'ooooxooi::'`         .:iiixkxxo'",
            "  'ooooi:'`                `'';ioxxo'",
            " 'i:'`                          '':io'",
            "'`                                   `'",
        ],
        "instantos": [
            "",
            "                                  ..,",
            "     'cx0XWWMMWNKOd:'.      ",
            "  .;kNMMMMMMMMMMMMMWNKd'    ",
            " 'kNMMMMWNNNWMMMMMMMMXo.    ",
            ",0MMMMMW0o;'..,:dKWMMMMMWx. ",
            "OMMMMMXl.        .xNMMMMMNo ",
            "WMMMMNl           .kWWMMMMO'",
            "MMMMMX;            oNWMMMMK,",
            "NMMMMWo           .OWMMMMMK,",
            "kWMMMMNd.        ,kWMMMMMMK,",
            "'kWMMMMWXxl:;;:okNMMMMMMMMK,",
            " .oXMMMMMMMWWWMMMMMMMMMMMMK,",
            "   'oKWMMMMMMMMMMMMMMMMMMMK,",
            "     .;lxOKXXXXXXXXXXXXXXXO;......",
            "          ................,d0000000kd:.",
            "                          .kMMMMMMMMMW0;",
            "                          .kMMMMMMMMMMMX",
            "                          .xMMMMMMMMMMMW",
            "                           cXMMMMMMMMMM0",
            "                            :0WMMMMMMNx,",
            "                             .o0NMWNOc.",
        ],
        "manjaro": [
            "██████████████████  ████████",
            "██████████████████  ████████",
            "██████████████████  ████████",
            "██████████████████  ████████",
            "████████            ████████",
            "████████  ████████  ████████",
            "████████  ████████  ████████",
            "████████  ████████  ████████",
            "████████  ████████  ████████",
            "████████  ████████  ████████",
            "████████  ████████  ████████",
            "████████  ████████  ████████",
            "████████  ████████  ████████",
            "████████  ████████  ████████",
        ],
        
        "fedora": [
            "             .',;::::;,'.",
            "         .';:cccccccccccc:;,.",
            "      .;cccccccccccccccccccccc;.",
            "    .:cccccccccccccccccccccccccc:.",
            "  .;ccccccccccccc;.:dddl:.;ccccccc;.",
            " .:ccccccccccccc;OWMKOOXMWd;ccccccc:.",
            ".:ccccccccccccc;KMMc;cc;xMMc;ccccccc:.",
            ",cccccccccccccc;MMM.;cc;;WW:;cccccccc,",
            ":cccccccccccccc;MMM.;cccccccccccccccc:",
            ":ccccccc;oxOOOo;MMMOOK.;cccccccccccc:",
            "cccccc;0MMKxdd:;MMMkddc.;cccccccccccc;",
            "ccccc;XM0';cccc;MMM.;ccccccccccccccc'",
            "ccccc;MMo;ccccc;MMW.;ccccccccccccccc;",
            "ccccc;0MNc.ccc.xMMd;ccccccccccccccc;",
            "cccccc;dNMWXXXWM0:;cccccccccccccc:,",
            "cccccccc;.:odl:.;cccccccccccccc:,.",
            ":cccccccccccccccccccccccccccc:'.",
            ".:cccccccccccccccccccccc:;,..",
            "  '::cccccccccccccc::;,.",
        ],
        
        "kubuntu": [
            "           `.:/ossyyyysso/:.",
            "        .:oyyyyyyyyyyyyyyyyyyo:`",
            "      -oyyyyyyydMMyyyyyyyysyyyyo-",
            "    -syyyyyyyyydMMoyyyyyydMMyyyyyys-",
            "   oyyyysdMyyyyydMMMMMMMMMMMMyyyyyyo",
            " `oyyyyydMMMMyyyysoooooodMMMMyyyyyyo`",
            " oyyyyyydMMMMyyyyyyyyyyyysdMMyssssyyyo",
            "-yyyyyyyyyydMyyyyyyyyyyyyyysdMMMMMysyyy-",
            "oyyyysoodMyyyyyyyyyyyyyyyyyyyydMMMMysyyyo",
            "yyyydMMMMMyyyyyyyyyyyyyyyyyyysosyyyyyyyy",
            "yyyydMMMMMyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "oyyyyysosdyyyyyyyyyyyyyyyyyyydMMMMysyyyo",
            "-yyyyyyyyyydMyyyyyyyyyyyyyysdMMMMMysyyy-",
            " oyyyyyydMMMyyyyyyyyyyyyyysdMMoyyyoyyyo",
            " `oyyyyydMMMyyyyyoooooodMMMMyyyyyyyo",
            "   oyyysyyoyyyysdMMMMMMMMMMyyyyyyyyo",
            "    -syyyyyyyyydMMMysyyydMMMyyyyyys-",
            "      -oyyyyyyyydMMyyyyyyysosyyyyo-",
            "        ./oyyyyyyyyyyyyyyyyyyo/.",
            "           `.:/oosyyyysso/:.`",
        ],
        
        "ubuntu": [
            "            .-/+oossssoo+\\-.",
            "        ´:+ssssssssssssssssss+:`",
            "      -+ssssssssssssssssssyyssss+-",
            "    .osssssssssssssssssdMMMNysssso.",
            "   /ssssssssssshdmmNNmmyNMMMMhssssss\\",
            "  +sssssssshm`yd`MMMMMMMNdddddyssssssss+",
            " /ssssssshNMMMyh`hyyyyhmNMMMNhssssssss\\",
            ".ssssssssdMMMNhssssssssshNMMMdssssssss.",
            "+sssshhhyNMMNyssssssssssyNMMMysssssss+",
            "ossyNMMMNyMMhsssssssssssshmmmhssssssso",
            "ossyNMMMNyMMhsssssssssssssshmmmhssssssso",
            "+sssshhhyNMMNyssssssssssssyNMMMysssssss+",
            ".ssssssssdMMMNhssssssssshNMMMdssssssss.",
            " \\ssssssshNMMMyhhhyyyyhdNMMMNhssssssss/",
            "  +sssssssssdm`yd`MMMMMMMMdddyssssssss+",
            "   \\ssssssssshdmNNNNmyNMMMMhssssss/",
            "    .osssssssssssssssdMMMNysssso.",
            "      -+ssssssssssssssssyyssss+-",
            "        `:+ssssssssssssssssss+:`",
            "            .-\\+oossssoo+/-.",
        ],
        
        "i3buntu": [
            "            .-/+oossssoo+\\-.",
            "        ´:+ssssssssssssssssss+:`",
            "      -+ssssssssssssssssssyyssss+-",
            "    .osssssssssssssssssdMMMNysssso.",
            "   /ssssssssssshdmmNNmmyNMMMMhssssss\\",
            "  +sssssssshm`yd`MMMMMMMNdddyssssssss+",
            " /ssssssshNMMMyh`hyyyyhmNMMMNhssssssss\\",
            ".ssssssssdMMMNhssssssssshNMMMdssssssss.",
            "+sssshhhyNMMNyssssssssssyNMMMysssssss+",
            "ossyNMMMNyMMhsssssssssssshmmmhssssssso",
            "ossyNMMMNyMMhsssssssssssssshmmmhssssssso",
            "+sssshhhyNMMNyssssssssssssyNMMMysssssss+",
            ".ssssssssdMMMNhssssssssshNMMMdssssssss.",
            " \\ssssssshNMMMyhhhyyyyhdNMMMNhssssssss/",
            "  +sssssssssdm`yd`MMMMMMMMdddyssssssss+",
            "   \\ssssssssshdmNNNNmyNMMMMhssssss/",
            "    .osssssssssssssssdMMMNysssso.",
            "      -+ssssssssssssssssyyssss+-",
            "        `:+ssssssssssssssssss+:`",
            "            .-\\+oossssoo+/-.",
        ],
        
        "linuxmint": [
            "             ...-:::::-...",
            "          .-MMMMMMMMMMMMMMM-.",
            "      .-MMMM`..-.:::::-..`MMMM-.",
            "    .:MMMM.:MMMMMMMMMMMMMMM:.MMMM:.",
            "   -MMM-M---MMMMMMMMMMMMMMMMMMM.MMM-",
            " `:MMM:MM`  :MMMM:....::-...-MMMM:MMM:`",
            " :MMM:MMM`  :MM:`  ``    ``  `:MMM:MMM:",
            ".MMM.MMMM`  :MM.  -MM.  .MM-  `MMMM.MMM.",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM:MMM:",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:",
            ".MMM.MMMM`  :MM:--:MM:--:MM:  `MMMM.MMM.",
            " :MMM:MMM-  `-MMMMMMMMMMMM-`  -MMM-MMM:",
            "  :MMM:MMM:`                `:MMM:MMM:",
            "   .MMM.MMMM:--------------:MMMM.MMM.",
            "     '-MMMM.-MMMMMMMMMMMMMMM-.MMMM-'",
            "       '.-MMMM``--:::::--``MMMM-.'",
            "            '-MMMMMMMMMMMMM-'",
            "               ``-:::::-``",
        ],
        
        "mint": [
            "             ...-:::::-...",
            "          .-MMMMMMMMMMMMMMM-.",
            "      .-MMMM`..-.:::::-..`MMMM-.",
            "    .:MMMM.:MMMMMMMMMMMMMMM:.MMMM:.",
            "   -MMM-M---MMMMMMMMMMMMMMMMMMM.MMM-",
            " `:MMM:MM`  :MMMM:....::-...-MMMM:MMM:`",
            " :MMM:MMM`  :MM:`  ``    ``  `:MMM:MMM:",
            ".MMM.MMMM`  :MM.  -MM.  .MM-  `MMMM.MMM.",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM:MMM:",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:",
            ".MMM.MMMM`  :MM:--:MM:--:MM:  `MMMM.MMM.",
            " :MMM:MMM-  `-MMMMMMMMMMMM-`  -MMM-MMM:",
            "  :MMM:MMM:`                `:MMM:MMM:",
            "   .MMM.MMMM:--------------:MMMM.MMM.",
            "     '-MMMM.-MMMMMMMMMMMMMMM-.MMMM-'",
            "       '.-MMMM``--:::::--``MMMM-.'",
            "            '-MMMMMMMMMMMMM-'",
            "               ``-:::::-``",
        ],
        
        "nixos": [
            "          ▗▄▄▄       ▗▄▄▄▄    ▄▄▄▖",
            "          ▜███▙       ▜███▙  ▟███▛",
            "           ▜███▙       ▜███▙▟███▛",
            "            ▜███▙       ▜██████▛",
            "     ▟█████████████████▙ ▜████▛     ▟▙",
            "    ▟███████████████████▙ ▜███▙    ▟██▙",
            "           ▄▄▄▄▖           ▜███▙  ▟███▛",
            "          ▟███▛             ▜██▛ ▟███▛",
            "         ▟███▛               ▜▛ ▟███▛",
            "▟███████████▛                  ▟██████████▙",
            "▜██████████▛                  ▟███████████▛",
            "      ▟███▛ ▟▙               ▟███▛",
            "     ▟███▛ ▟██▙             ▟███▛",
            "    ▟███▛  ▜███▙           ▝▀▀▀▀",
            "    ▜██▛    ▜███▙ ▜██████████████████▛",
            "     ▜▛     ▟████▙ ▜████████████████▛",
            "           ▟██████▙       ▜███▙",
            "          ▟███▛▜███▙       ▜███▙",
            "         ▟███▛  ▜███▙       ▜███▙",
            "         ▝▀▀▀    ▀▀▀▀▘       ▀▀▀▘",
        ],
        
        "popos": [
            "             /////////////",
            "         /////////////////////",
            "      ///////*767////////////////",
            "    //////7676767676*//////////////",
            "   /////76767//7676767//////////////",
            "  /////767676///76767///////////////",
            " ///////767676///76767.///7676*///////",
            "/////////767676//76767///767676////////",
            "//////////76767676767////76767/////////",
            "///////////76767676//////7676//////////",
            "////////////,7676,///////767///////////",
            "/////////////76767///////76////////////",
            "///////////////7676////////////////////",
            " ///////////////7676///767////////////",
            "  //////////////////////'////////////",
            "   //////.7676767676767676767,//////",
            "    /////767676767676767676767/////",
            "      ///////////////////////////",
            "         /////////////////////",
            "             /////////////",
        ],
        
        "pop_os": [
            "             /////////////",
            "         /////////////////////",
            "      ///////*767////////////////",
            "    //////7676767676*//////////////",
            "   /////76767//7676767//////////////",
            "  /////767676///76767///////////////",
            " ///////767676///76767.///7676*///////",
            "/////////767676//76767///767676////////",
            "//////////76767676767////76767/////////",
            "///////////76767676//////7676//////////",
            "////////////,7676,///////767///////////",
            "/////////////76767///////76////////////",
            "///////////////7676////////////////////",
            " ///////////////7676///767////////////",
            "  //////////////////////'////////////",
            "   //////.7676767676767676767,//////",
            "    /////767676767676767676767/////",
            "      ///////////////////////////",
            "         /////////////////////",
            "             /////////////",
        ],
    }
    
    # ASCII art per le principali distribuzioni Linux
    LINUX_DISTROS = {
        "ubuntu": [
            "            .-.           ",
            "         .-'``(   )_      ",
            "      ,`\\ \\    `-'  (_)   ",
            "     /   \\ '    .____     ",
            "    /     \\    /    /_\\   ",
            "   /       \\  /  _  `--'  ",
            "  /         \\/ ( (     )  ",
            " /           \\   `-.   )_ ",
            "/          __/      `-`--'",
            "`-.___..--(                  ",
        ],
        "debian": [
            "       _,met$$$$$gg.          ",
            "    ,g$$$$$$$$$$$$$$$P.       ",
            "  ,g$$P\"     \"\"\"Y$$.\"         ",
            " ,$$P'              `$$$.      ",
            "',$$P       ,ggs.     `$$b:    ",
            "`d$$'     ,$P\"'   .    $$$     ",
            " $$P      d$'     ,    $$P     ",
            " $$:      $$.   -    ,d$$'     ",
            " $$;      Y$b._   _,d$P'       ",
            " Y$$.    `.`\"Y$$$$P\"'          ",
            " `$$b      \"-.__               ",
            "  `Y$$                         ",
            "   `Y$$.                       ",
            "     `$$b.                     ",
            "       `Y$$b.                  ",
            "          `\"Y$b._              ",
            "              `\"\"\"             ",
        ],
        "arch": [
            "                   -`                 ",
            "                  .o+`                ",
            "                 `ooo/                ",
            "                `+oooo:               ",
            "               `+oooooo:              ",
            "               -+oooooo+:             ",
            "             `/:-:++oooo+:            ",
            "            `/++++/+++++++:           ",
            "           `/++++++++++++++:          ",
            "          `/+++ooooooooooooo/`        ",
            "         ./ooosssso++osssssso+`       ",
            "        .oossssso-````/ossssss+`      ",
            "       -osssssso.      :ssssssso.     ",
            "      :osssssss/        osssso+++.    ",
            "     /ossssssss/        +ssssooo/-    ",
            "   `/ossssso+/:-        -:/+osssso+-  ",
            "  `+sso+:-`                 `.-/+oso: ",
            " `++:.                           `-/+/",
            " .`                                 `/",
        ],
        "fedora": [
            "           :/------------://          ",
            "        :------------------://        ",
            "      :-----------/shhdhyo/-:///      ",
            "    /-----------omMMMNNNMMMd/-:/      ",
            "   :-----------sMMMMNMNMP.MMM/-:/     ",
            "  :-----------:MMMdP-------/:--:/     ",
            " ,------------:MMMd--------:--:/      ",
            " :------------:MMMd-------:--:/       ",
            " :----..------/+MMMmo------:--:/      ",
            " :---.---.-----:yMMM+------:--:/      ",
            " :--.-------.---:oso:------:--:/      ",
            " :--...--------::::-------:--:/       ",
            " :--.------------:--------:--:/       ",
            " :--.-------------:-------:--:/       ",
            " :--.---------------:-----:--:/       ",
            " :--.----------------:----:--:/       ",
            " :--.----------------:---:--:/        ",
            " :--.---------------:---:--:/         ",
            " :--.-------------:---:--:/           ",
            " :--.------------:---:--:/            ",
            " :--.-----------:---:--:/             ",
            " :--------------:--:--:/              ",
            " :------------:---:--:/               ",
            " :----------:-----:/                  ",
            " :---------:------/                   ",
        ],
    }
    
    def __init__(self, config, ascii_file=None, ascii_distro=None, use_color=True):
        """Inizializza la classe AsciiArt."""
        self.os_type = platform.system().lower()  # windows, linux, darwin
        self.config = config
        self.use_color = use_color
        
        # Determina l'ASCII art da utilizzare
        self.ascii = None
        if (ascii_file):
            # Utilizza un file ASCII personalizzato
            self.ascii = self._load_ascii_from_file(ascii_file)
        elif (ascii_distro):
            # Utilizza una distribuzione ASCII specificata
            self.ascii = self._get_ascii_for_distro(ascii_distro)
        else:
            # Auto-rilevamento
            self.ascii = self._auto_detect_ascii()
            
        # Se non è stato trovato nulla, utilizza il generico
        if not self.ascii:
            self.ascii = self.ASCII_ART["generic"]
            
        # Determina il colore da utilizzare
        self.color = self._determine_color()
            
    def _load_ascii_from_file(self, file_path):
        """Carica l'ASCII art da un file."""
        try:
            with open(file_path, 'r') as f:
                return [line.rstrip('\n') for line in f.readlines()]
        except Exception as e:
            print(f"Errore nel caricamento del file ASCII: {e}")
            return None
            
    def _get_ascii_for_distro(self, distro):
        """Restituisce l'ASCII art per una distribuzione specifica."""
        # Controllo nel dizionario delle distribuzioni Linux
        if distro.lower() in self.LINUX_DISTROS:
            return self.LINUX_DISTROS[distro.lower()]
            
        # Controllo nel dizionario principale
        if distro.lower() in self.ASCII_ART:
            return self.ASCII_ART[distro.lower()]
            
        # Se non viene trovato nulla, restituisce None
        return None
        
    def _auto_detect_ascii(self):
        """Auto-rileva l'ASCII art da utilizzare in base al sistema."""
        if self.os_type == "linux":
            # Rileva la distribuzione Linux
            distro = self._detect_linux_distro()
            if distro and distro.lower() in self.LINUX_DISTROS:
                return self.LINUX_DISTROS[distro.lower()]
                
        # Altrimenti usa l'ASCII art per il sistema operativo
        if self.os_type in self.ASCII_ART:
            return self.ASCII_ART[self.os_type]
        
        # Fallback al generico
        return self.ASCII_ART["generic"]
        
    def _detect_linux_distro(self):
        """Rileva la distribuzione Linux."""
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        return line.split("=")[1].strip().strip('"')
        except:
            pass
        
        return None
        
    def _determine_color(self):
        """Determina il colore da utilizzare per l'ASCII art."""
        # Se i colori sono disabilitati, restituisci vuoto
        if not self.use_color:
            return ""
            
        # Altrimenti usa il colore predefinito per il sistema operativo
        color_name = self.DEFAULT_COLORS.get(self.os_type, "white")
        return self.COLORS.get(color_name, self.COLORS["reset"])
        
    def _colorize(self, text):
        """Applica il colore al testo."""
        if not self.use_color:
            return text
        return f"{self.color}{text}{self.COLORS['reset']}"
        
    def _format_info_line(self, label, value):
        """Formatta una riga di informazioni."""
        if not self.use_color:
            return f"{label}: {value}"
        
        # Colora solo l'etichetta
        colored_label = f"{self.color}{label}{self.COLORS['reset']}"
        return f"{colored_label}: {value}"
        
    def print_with_info(self, info):
        """Stampa l'ASCII art con le informazioni di sistema."""
        # Preparare le righe di informazioni
        info_lines = []
        
        # User@hostname
        user_host = f"{self._colorize(info.get('user', 'user'))}@{self._colorize(info.get('hostname', 'host'))}"
        info_lines.append(user_host)
        info_lines.append("-" * len(user_host.replace("\033[0m", "").replace(self.color, "")))
        
        # Sistema operativo
        if "os" in info:
            info_lines.append(self._format_info_line("OS", info["os"]))
            
        # Kernel
        if "kernel" in info:
            info_lines.append(self._format_info_line("Kernel", info["kernel"]))
            
        # Uptime
        if "uptime" in info:
            info_lines.append(self._format_info_line("Uptime", info["uptime"]))
            
        # Pacchetti
        if "packages" in info and info["packages"]:
            packages_str = ", ".join([f"{count} ({name})" for name, count in info["packages"].items()])
            info_lines.append(self._format_info_line("Packages", packages_str))
            
        # Shell
        if "shell" in info:
            info_lines.append(self._format_info_line("Shell", info["shell"]))
            
        # Risoluzione
        if "resolution" in info:
            info_lines.append(self._format_info_line("Resolution", info["resolution"]))
            
        # DE/WM
        if "de" in info:
            info_lines.append(self._format_info_line("DE", info["de"]))
        if "wm" in info:
            info_lines.append(self._format_info_line("WM", info["wm"]))
            
        # Terminale
        if "terminal" in info:
            info_lines.append(self._format_info_line("Terminal", info["terminal"]))
            
        # CPU
        if "cpu" in info:
            cpu = info["cpu"]
            cpu_str = f"{cpu.get('model', 'Unknown')} ({cpu.get('cores', '?')}C/{cpu.get('threads', '?')}T) {cpu.get('usage', '')}"
            info_lines.append(self._format_info_line("CPU", cpu_str))
            
        # GPU
        if "gpu" in info and "model" in info["gpu"]:
            gpu_model = info["gpu"]["model"]
            
            # Gestire caso GPU multiple con vari separatori
            separators = ["/", "+", ",", ";", "e", "and", "&"]
            is_multi_gpu = any(sep in gpu_model for sep in separators)
            
            if is_multi_gpu:
                # Prima verifica se c'è separatore "/"
                if "/" in gpu_model:
                    gpu_models = gpu_model.split("/")
                # Altrimenti prova con altri separatori
                elif "+" in gpu_model:
                    gpu_models = gpu_model.split("+")
                elif "," in gpu_model:
                    gpu_models = gpu_model.split(",")
                elif ";" in gpu_model:
                    gpu_models = gpu_model.split(";")
                elif " e " in gpu_model.lower():
                    gpu_models = gpu_model.lower().split(" e ")
                elif " and " in gpu_model.lower():
                    gpu_models = gpu_model.lower().split(" and ")
                elif "&" in gpu_model:
                    gpu_models = gpu_model.split("&")
                else:
                    # Fallback se non trova separatori ma è troppo lungo
                    if len(gpu_model) > 50:  # Aumentato il limite per catturare righe più lunghe
                        # Cerca di dividere su newlines se presenti
                        if "\n" in gpu_model:
                            gpu_models = gpu_model.split("\n")
                        else:
                            # Dividi in parti più piccole
                            mid = len(gpu_model) // 2
                            gpu_models = [gpu_model[:mid], gpu_model[mid:]]
                    else:
                        gpu_models = [gpu_model]
                
                # Pulisci ogni modello di GPU e visualizza
                for i, model in enumerate(gpu_models):
                    model = model.strip()
                    if not model:  # Salta modelli vuoti
                        continue
                        
                    # Capitalizza la prima lettera se non è così
                    if model and model[0].islower():
                        model = model[0].upper() + model[1:]
                        
                    # Corretto: mostra sempre GPU correttamente numerato
                    label = "GPU" if i == 0 else f"GPU {i+1}"
                    info_lines.append(self._format_info_line(label, model))
            else:
                # Caso singola GPU
                info_lines.append(self._format_info_line("GPU", gpu_model))
            
        # Memoria
        if "memory" in info:
            mem = info["memory"]
            mem_str = f"{mem.get('used', '?')} / {mem.get('total', '?')} ({mem.get('percent', '?')})"
            info_lines.append(self._format_info_line("Memory", mem_str))
            
        # Disco
        if "disk" in info and "error" not in info["disk"]:
            disk = info["disk"]
            disk_str = f"{disk.get('used', '?')} / {disk.get('total', '?')} ({disk.get('percent', '?')})"
            info_lines.append(self._format_info_line("Disk", disk_str))
            
        # Temperature (se disponibile)
        if "temperatures" in info and info["temperatures"]:
            for sensor, temp in list(info["temperatures"].items())[:2]:  # Solo le prime due temperature
                info_lines.append(self._format_info_line(f"Temp ({sensor})", temp))
        
        # Aggiungi riga dei colori alla fine
        if self.use_color:
            color_blocks = ""
            for color in ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]:
                color_blocks += f"{self.COLORS[color]}███{self.COLORS['reset']}"
            info_lines.append("")  # Riga vuota
            info_lines.append(color_blocks)
            
        # Calcola la massima lunghezza dell'ASCII art
        max_ascii_length = max(len(line) for line in self.ascii)
        
        # Prepara le righe per la visualizzazione affiancata
        display_lines = []
        for i in range(max(len(self.ascii), len(info_lines))):
            ascii_line = self._colorize(self.ascii[i]) if i < len(self.ascii) else " " * max_ascii_length
            info_line = info_lines[i] if i < len(info_lines) else ""
            
            # Calcola la spaziatura (tieni conto dei codici colore)
            padding = max_ascii_length - len(self.ascii[i]) if i < len(self.ascii) else max_ascii_length
            display_lines.append(f"{ascii_line}{' ' * padding}  {info_line}")
            
        # Stampa il tutto
        print("\n".join(display_lines))