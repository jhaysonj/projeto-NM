# EXECUTE O SCRIPT COMO SUPER USUARIO

import os

canal = str(input("digite o canal:"))
canal2ghz = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
canal5ghz = ["36", "40", "44", "48", "52", "56", "60", "64", "100", "104", "108", "112", "116", "120", "124", "128", "132", "136", "140", "149", "153"]


while ((canal.isdecimal() == False) or (canal not in canal2ghz and canal not in canal5ghz)):
    canal = str(input("canal invalido, escolha outro canal:"))

# coloca a placa em modo de monitoramento
os.system("airmon-ng start wlan0")

# derruba a placa 
os.system("ifconfig wlan0 down")

# troca de canal
os.system(f"iwconfig wlan0 channel {canal}")

# sobe a placa
os.system("ifconfig wlan0 up")

# mostra o canal atual da placa
os.system("iwlist wlan0 channel")