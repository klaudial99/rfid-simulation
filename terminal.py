#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from functions import *
from tkinter import *

# domyślne id terminala
terminal_id = "1"

# nazwa brokera
broker = "DESKTOP-HPMOF2G"

#TLS port
port = 8883

# klient MQTT
client = mqtt.Client()

# okno z przyciskami, symulującymi zeskanowanie karty
window = Tk()

# funkcja pozwalająca na wybór terminala, z którgo użytkownik chce korzystać
def chooseTerminal():
    print("CHOOSING A TERMINAL")
    connect()
    printTerminals()
    global terminal_id
    terminal_id = input("Enter id of terminal you want to use\n")


def callWorker(card_id):
    # publikuje wiadomości o określonym tamacie i z określonymi danymi
    client.publish("worker/name", card_id + "." + terminal_id,)


# stworzenie przycisków, nadanie im działania i umieszczenie w głównym oknie
def createMainWindow():
    window.geometry("250x70")
    window.title("TERMINAL " + terminal_id)

    intro_label = Label(window, text="Enter card ID:")
    intro_label.grid(row=0, column=0)
    id = Entry(window)
    id.grid(row=0, column=1)
    button_enter = Button(window, text="Enter", command=lambda: callWorker(id.get()))
    button_enter.grid(row=1, column=1)

    button_stop = Button(window, text="Stop", command=window.quit)
    button_stop.grid(row=1, column=0)


def connectToBroker():
    # ustawienia TLS
    client.tls_set("ca.crt")  #plik certyfikatu
    # uwierzytenienie
    client.username_pw_set(username='client', password='password')
    # połączenie się z brokerem
    client.connect(broker, port)
    # wysłanie wiadomości o połączeniu
    callWorker("Client connected")


def disconnectFromBroker():
    # wysłanie wiadomości o rozłączeniu
    callWorker("Client disconnected")
    # rozłączenie klienta
    client.disconnect()


def runSender():
    chooseTerminal()
    connectToBroker()
    createMainWindow()
    # wyświetlanie głownego okna
    window.mainloop()
    disconnectFromBroker()


if __name__ == "__main__":
    runSender()
