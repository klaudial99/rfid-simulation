from datetime import *
from tabulate import tabulate
import sqlite3

# utworzenie połączenia z bazą danych
connection = 0


def connect():

    global connection
    connection = sqlite3.connect("database.db", check_same_thread=False)

# utworzenie tabel w bazie danych
def createTables():
    # tabela przechowująca użytkowników
    tableUsers = """CREATE TABLE `users` (
                    `idU` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    `name` VARCHAR(20) NOT NULL,
                    `surname` VARCHAR(20) NOT NULL
                    ) """

    # tabela przechowujaca karty
    tableCards = """CREATE TABLE `cards` (
                    `idC` INTEGER NOT NULL PRIMARY KEY,
                    `userId` INTEGER
                    )"""

    # tabela przechowująca terminale
    tableTerminals = """CREATE TABLE `terminals` (
                        `idT` INTEGER NOT NULL PRIMARY KEY
                        )"""

    # tabela przechowująca pojedyncze skany karty
    tableScans = """CREATE TABLE `scans` (
                    `idS` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    `cardId` INTEGER NOT NULL,
                    `userId` INTEGER,
                    `terminalId` INTEGER NOT NULL,
                    `time` TIMESTAMP  NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')) 
                    )"""

    #tabela par logowań-wylogowań, przechowująca dodatkowo czas zalogowania w systemie
    tablePairs = """CREATE TABLE `pairs` (
                    `idP` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    `cardId` INTEGER NOT NULL,
                    `userId` INTEGER,
                    `startTime` DATETIME NOT NULL,
                    `stopTime` DATETIME NOT NULL,
                    `time` TIME NOT NULL
                    )"""

    # obiekt za pomocą którego łączę się z bazą danych
    cursor = connection.cursor()
    cursor.execute(tableUsers)
    cursor.execute(tableCards)
    cursor.execute(tableTerminals)
    cursor.execute(tableScans)
    cursor.execute(tablePairs)
    # wysyła potwierdzenie operacji z execute(), Python nie robi tego automatycznie
    # dlatego po każdej zmianie w bazie danych należy użyć tej komendy
    connection.commit()


# funkcja tworząca listę list, potrzebna do skorzystania z biblioteki tabulate
def tablePrinting(list):
    newList = []
    for i in list:
        insideList = []
        for j in i:
            insideList.append(j)
        newList.append(insideList)
    return newList


# zwraca w tablicy nazwy kolumn z tabeli o podanej nazwie
def namesOfColumns(tableName):
    cursor = connection.cursor()
    sql = ("SELECT * FROM %s" % (tableName))
    table = []
    for column in cursor.execute(sql).description:
        table.append(column)
    headers = []
    for i in table:
        headers.append(i[0])
    return headers


def printUsers():

    cursor = connection.cursor()
    # wykonanie SQLowej operacji
    # w tym wypadku wypisanie tabeli "users"
    cursor.execute("SELECT * FROM `users`")
    # fetchall() bierze wszystkie rekordy z wyniku powyższej operacji i tworzy z nich listę krotek
    result = cursor.fetchall()
    print("Existing users: ")
    print(tabulate(tablePrinting(result), namesOfColumns("users"), tablefmt="psql"))

    connection.commit()


# analogicznie wypisuje tabelę "cards"
def printCards():

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `cards`")
    result = cursor.fetchall()
    print("Existing cards: ")
    print(tabulate(tablePrinting(result), namesOfColumns("cards"), tablefmt="psql"))
    connection.commit()


# analogicznie wypisuje tabelę "terminals"
def printTerminals():

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `terminals`")
    result = cursor.fetchall()
    print("Existing terminals: ")
    print(tabulate(tablePrinting(result), namesOfColumns("terminals"), tablefmt="psql"))
    connection.commit()


# analogicznie wypisuje tabelę "scans"
def printScans():

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `scans`")
    result = cursor.fetchall()
    print("Existing scans: ")
    print(tabulate(tablePrinting(result), namesOfColumns("scans"), tablefmt="psql"))
    connection.commit()


# analogicznie wypisuje tabelę "pairs"
def printPairs():

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `pairs`")
    result = cursor.fetchall()
    print("Existing pairs of login & logout: ")
    print(tabulate(tablePrinting(result), namesOfColumns("pairs"), tablefmt="psql"))
    connection.commit()


# tworzenie pracownika z kodu
def addUserAuto(name, surname):

    cursor = connection.cursor()
    sql = "INSERT INTO `users` (`name`, `surname`) VALUES (?, ?)"
    cursor.execute(sql, (name, surname))
    connection.commit()



# tworzenie karty z kodu
def addCardAuto(cardID, userID):

    cursor = connection.cursor()
    sql = "INSERT INTO `cards` VALUES (?, ?)"
    cursor.execute(sql, (cardID, userID))
    connection.commit()



# tworzenie terminala z kodu
def addTerminalAuto(terminalID):

    cursor = connection.cursor()
    sql = "INSERT INTO `terminals` VALUES (?)"
    cursor.execute(sql, (terminalID))
    connection.commit()


# zestaw początkowych danych, wprowadzanych do bazy danych przy jej tworzeniu
def startData():
    addUserAuto("Jan", "Kowalski")
    addUserAuto("Adrian", "Nowak")
    addUserAuto("Agnieszka", "Stankiewicz")
    addUserAuto("Klaudia", "Laskowska")
    addUserAuto("Teresa", "Niedziela")

    addCardAuto("111", None)
    addCardAuto("222", "2")
    addCardAuto("333", "3")
    addCardAuto("444", "4")
    addCardAuto("555", "5")
    addCardAuto("666", None)

    addTerminalAuto("1")
    addTerminalAuto("2")


# dodawanie użytkownika z klawiatury
def addUser():

    cursor = connection.cursor()
    print("ADDING A USER")

    # wypisuję najpierw dodanych już użytkowników, żeby był wgląd
    # i np. przypadkiem nie dodać 2x tej samej osoby
    # tę samą technikę będe stosować dalej przy każdej interaktywnej funkcji
    printUsers()

    # pobranie danych z klawiatury
    name = input("Enter your name: \n")
    surname = input("Enter your surname: \n")

    # dodanie do bazy danych użytkownika o podanych danych
    sql = "INSERT INTO `users` (`name`, `surname`) VALUES (?, ?)"
    cursor.execute(sql, (name, surname))
    connection.commit()


# dodawanie karty z klawiatury
def addCard():
    cursor = connection.cursor()

    print("ADDING A CARD")

    printCards()
    # pobranie danych z klawiatury
    id = input("Scan your card! <enter id of your card> \n")

    assignYN = input("Would you like to assign it to a user? Enter 'y' or 'n'.\n")
    # jeśli chcemy od razu przypisać użytkownika do karty
    if assignYN == "y":
        userYN = input("Does the user already exists? Enter 'y' or 'n'.\n")

        # jeśli użytkownik już istnieje
        if userYN == "y":
            printUsers()
            # pobranie danych z klawiatury
            userId = input("Enter ID of choosen user: \n")

            # dodanie karty z przypisaniem do użytkownika
            sql = "INSERT INTO `cards` VALUES (?, ?)"
            cursor.execute(sql, (id, userId))
            connection.commit()

        # jeśli użytkownik, którego chcemy wybrać jeszcze nie istnieje
        elif userYN == "n":
            # dodawanie nowego użytkownika
            addUser()
            connection.commit()

            # wybranie użytkownika o największym ID czyli ostatnio dodanego
            # i dodanie karty z tym przypisanym użytkownikiem do bazy danych
            cursor.execute("SELECT MAX(`idU`) FROM `users`")
            userId = cursor.fetchone()
            sql = "INSERT INTO `cards` VALUES (?, ?)"
            cursor.execute(sql, (id, userId[0]))
            connection.commit()

        # w przypadku błędnej komendy
        else:
            print("Wrong typing! Let's try once again.")

    # jeśli nie chcemy przypisywać użytkownika do karty
    elif assignYN == "n":
        # dodajemy kartę bez przypisanego ID pracownika
        sql = "INSERT INTO `cards` VALUES (%s, NULL)" % (id)
        print(id)
        cursor.execute(sql)
        connection.commit()

    # w przypadku błędnej komendy
    else:
        print("Wrong typing! Let's try once again.")


# dodawanie przypisania z klawiatury
def addAssignment():
    cursor = connection.cursor()

    print("ADDING NEW ASSIGNMENT")

    # wybór i wypisanie wszystkich nieprzypisanych kart
    cursor.execute("SELECT * FROM `cards` WHERE `userId` IS NULL")
    result = cursor.fetchall()
    print("Cards without assignment: ")
    print(tabulate(tablePrinting(result), namesOfColumns("cards"), tablefmt="psql"))
    # pobranie danych z klawiatury
    idCard = input("Enter ID of a card you want to assign.\n")

    # w exist przechowywana lista z kartą o podanym ID o ile nie ma przypisania
    sql = "SELECT * FROM `cards` WHERE `idC`=%s AND `userId` IS NULL" % (idCard)
    cursor.execute(sql)
    exists = cursor.fetchall()

    # jeśli exist nie jest pusty
    if exists:
        #printUsers()
        sql = "SELECT idU, name, surname FROM users LEFT JOIN cards ON cards.userId = users.idU WHERE cards.userid IS NULL"
        #sql = "SELECT * FROM `users` EXCEPT SELECT idU, name, surname FROM `users` JOIN `cards` ON users.idU = cards.userId"
        cursor.execute(sql)
        result = cursor.fetchall()

        print("Users without any assigned cards:")
        print(tabulate(tablePrinting(result), namesOfColumns("users"), tablefmt="psql"))
        # pobranie danych z klawiatury
        idUser = input("Choose ID of a person you want to assign to the card.\n")

        # sprawdzenie czy wybranu uzytkownik nie jest już przypisany do jakiejś karty
        cursor.execute("SELECT `userId` FROM `cards`")
        result = cursor.fetchall()
        free = True
        for i in result:
            if str(i[0]) == idUser:
                free = False
        # jeśli nie jest, to następuje przypisanie karty do użytkownika
        if free:
            # przypisanie podanego ID użytkownika do karty
            cursor.execute("UPDATE `cards` SET `userId`=%s WHERE `idC`= %s" % (idUser, idCard))
        # w przeciwnym razie komunikat
        else:
            print("This user is already assigned to the card!")
    # jeśli jest pusty to wiadomość, że jest już przypisany użytkownik do karty
    else:
        print("The card is already assigned! You have to delete the assignment first.")

    connection.commit()


# usuwanie przypisania z klawiatury
def deleteAssignment():

    cursor = connection.cursor()
    print("DELETING AN ASSIGNMENT")

    # wybór i wypisanie kart, które mają przypisanego użytkownika
    cursor.execute("SELECT * FROM `cards` WHERE `userId` IS NOT NULL")
    result = cursor.fetchall()
    print("Existing assignments: ")
    print(tabulate(tablePrinting(result), namesOfColumns("users"), tablefmt="psql"))

    # pobranie danych z klawiatury
    id = input("Scan a card which user assignment you want to remove <enter id of a card>\n")

    # usunięcie przypisania osoby do karty
    cursor.execute("UPDATE `cards` SET `userId`=NULL WHERE `idC`= %s" % (id))
    connection.commit()


# dodawanie terminala z klawiatury
def addTerminal():

    cursor = connection.cursor()
    print("ADDING A TERMINAL")

    printTerminals()

    # pobranie danych z klawiatury
    id = input("Enter ID of a new terminal: \n")

    # sprawdzenie czy terminal o podanym id znajduje się już w bazie
    cursor.execute("SELECT * FROM `terminals`")
    result = cursor.fetchall()
    free = True
    for i in result:
        if str(i[0]) == id:
            free = False
    # jeśli nie
    if free:
        # dopisanie nowego terminala do bazy danych
        sql = "INSERT INTO `terminals` VALUES (?)"
        cursor.execute(sql, (id))
        connection.commit()
    # przeciwnym wypadku komunikat
    else:
        print("This terminal already exists!")


# usuwanie terminala z klawiatury
def deleteTerminal():

    cursor = connection.cursor()
    print("DELETING A TERMINAL")

    printTerminals()

    # pobranie danych z klawiatury
    id = input("Enter ID of terminal you want to delete: \n")

    # usunięcie z bazy danych terminala o wskazanym ID
    cursor.execute("DELETE FROM `terminals` WHERE `idT`= %s" % (id))
    connection.commit()


# skanowanie karty, funkcja, którą wykorzystuje terminal
def scanCard(id, terminalId):

    cursor = connection.cursor()
    # wzięcie ID użytkownika przypisanego do karty o podanym iD i przypisanie do zmiennej
    cursor.execute("SELECT `userId` FROM `cards` WHERE `idC`=%s" % (id))
    idU = cursor.fetchone()
    #jeśli karta o podanym ID nie istnieje, to zmieniam None na krotkę zawierającą None
    #czyli na wynik wzięcia idU karty bez przypisanego użytkonika, żeby potem argumenty przy dodawaniu sie zgadzały
    if(idU==None):
        idU=(None,)
    # sprawdzenie czy dane skanowanie to logowanie czy wylogowanie
    # modulo=0 - logowanie; modulo=1 - wylogowanie
    cursor.execute("SELECT COUNT(`cardId`) FROM `scans` WHERE `cardId`=%s" % (id))
    modulo = cursor.fetchone()
    modulo = int(modulo[0]) % 2
    # dodanie skanu dla podanej karty i terminala
    sql = "INSERT INTO `scans` (`cardId`, `userId`, `terminalId`)VALUES (?, ?, ?)"
    cursor.execute(sql, (id, idU[0], terminalId))
    connection.commit()

    # jeśli jest to wylogowanie
    if modulo == 1:
        # wybranie skanów danej karty posortowane malejąco po czasie
        sql = "SELECT time FROM `scans` WHERE `cardId`=%s ORDER BY time DESC LIMIT 2 " % (id)
        cursor.execute(sql)
        result = cursor.fetchall()
        # dodanie do tabeli par logowań i wylogowań rekordu z aktualnym wylogowaniem
        sql = "INSERT INTO `pairs` (`cardId`, `userId`, `startTime`, `stopTime`, `time`)VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, (
            id, idU[0], result[1][0], result[0][0], str(datetime.strptime(result[0][0], '%Y-%m-%d %H:%M:%S') - datetime.strptime(result[1][0], '%Y-%m-%d %H:%M:%S'))))

        connection.commit()


# utworzneie raportu z klawiatury
def makeRaport():

    cursor = connection.cursor()
    print("MAKING A RAPORT")

    sql = "SELECT idU, name, surname, idC FROM users LEFT JOIN cards ON cards.userId = users.idU "
    cursor.execute(sql)
    result = cursor.fetchall()
    print(tabulate(tablePrinting(result), ["idU", "name", "surname", "idC"], tablefmt="psql"))

    # pobranie danych z klawiatury
    id = input("Enter ID of a user for whom you want to make a raport\n")

    # wyszukanie osoby o podanym ID
    cursor.execute("SELECT * FROM `users` WHERE `idU`=%s" % (id))
    result = cursor.fetchone()
    # "wyciągnięcie" imienia i nazwiska i przypisanie do zmiennych
    name = result[1]
    surname = result[2]

    # wybór i wypisanie rekordów dla pracownika o podanym ID
    cursor.execute("SELECT * FROM `pairs` WHERE `userId`=%s" % (id))
    result = cursor.fetchall()
    print("RAPORT FOR: ", name, surname)
    print(tabulate(tablePrinting(result), namesOfColumns("pairs"), tablefmt="psql"))
    connection.commit()
