from functions import *
import paho.mqtt.client as mqtt
import time
import os

# nazwa brokera
broker = "DESKTOP-HPMOF2G"

#TLS port
port = 8883

# klient MQTT
client = mqtt.Client()


def processMessage(client, userdata, message):
    # zdekodoawanie wiaodmości
    message = (str(message.payload.decode("utf-8"))).split(".")

    # wypisanie odczytanych danych w odpowiednim formacie
    if message[0] != "Client connected" and message[0] != "Client disconnected":
        print("At", time.ctime(), "card", message[0], "has been used in terminal number", message[1])
        scanCard(message[0], message[1])
    else:
        print(message[0] + ": " + message[1])


def connectToBroker():
    # ustawienia TLS
    client.tls_set("ca.crt")
    # uwierzytenienie
    client.username_pw_set(username='server', password='password')
    # połączenie z brokerem
    client.connect(broker, port)
    # przetwarzanie wiadomości
    client.on_message = processMessage
    # aktywowanie klienta i włączenie subskrypcji określonego tematu
    client.loop_start()
    client.subscribe("worker/name")


# odłączneie klienta od brokera
def disconnectFromBroker():
    client.loop_stop()
    client.disconnect()


# menu wyboru, potwierdzenie enterem
def menu():
    print("MENU:")
    print("1. Add new user.")
    print("2. Add new card.")
    print("3. Add user assignment.")
    print("4. Delete user assignment.")
    print("5. Add new terminal.")
    print("6. Delete terminal.")
    print("7. Show existing users.")
    print("8. Show existing cards.")
    print("9. Show existing terminals.")
    print("10. Show existing scans.")
    print("11. Show existing pairs of login & logout.")
    print("12. Make raport.")
    print("13. Exit the programme")
    print("Enter a number corresponding to the action you want to activate.")
    number = int(input())
    if number == 1:
        addUser()
        menu()
    elif number == 2:
        addCard()
        menu()
    elif number == 3:
        addAssignment()
        menu()
    elif number == 4:
        deleteAssignment()
        menu()
    elif number == 5:
        addTerminal()
        menu()
    elif number == 6:
        deleteTerminal()
        menu()
    elif number == 7:
        printUsers()
        menu()
    elif number == 8:
        printCards()
        menu()
    elif number == 9:
        printTerminals()
        menu()
    elif number == 10:
        printScans()
        menu()
    elif number == 11:
        printPairs()
        menu()
    elif number == 12:
        makeRaport()
        menu()
    elif number == 13:
        return
    else:
        print("Wrong typing! Let's try once again.")
        menu()


if __name__ == "__main__":
    # ifa można zakomentować za >=2 użyciem kodu
    if os.path.exists("database.db"):
        os.remove("database.db")
    connect()
    connectToBroker()
    # dwie kolejne funckje można zakomentować za >=2 użyciem kodu
    createTables()
    startData()
    menu()
    disconnectFromBroker()
