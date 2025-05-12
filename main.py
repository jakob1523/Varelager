from tabulate import tabulate
import random 
import mariadb

print('''
Brukernavn admin bruker = varelager
Passord admin bruker = 123

Brukernavn normal bruker = varese
Passord normal bruker = 321      
''')

brukernavn = input("Skriv brukernavn: ")

passord = input("Skriv passord: ")

#Brukernavn admin bruker = varelager
#Passord admin bruker = 123

#Brukernavn normal bruker = varese
#Passord normal bruker = 321

DB_CONFIG = {
    'host': '10.2.2.9',
    'user': brukernavn,
    'password': passord,
    'database': 'varelager'
}

def get_db_connection():
    return mariadb.connect(**DB_CONFIG)

def meny():
    print('''
        ****************************
        |1 Legg til vare
        |2 Slett vare
        |3 Søk ettet vare
        |4 Juster vare
        |5 Se alle varer
        |6 Se varelogg
        |7 Avslutt
        ****************************            
          ''')

    valg = int(input("Velg en av alternativene ovenfor: "))

    if valg == 1:
        leggVare()

    elif valg == 2:
        slettVare()
    
    elif valg == 3:
        sookVare()
    
    elif valg == 4:
        justerVare()
    
    elif valg == 5:
        seVarer()

    elif valg == 6:
        seVarelogg()

    elif valg == 7:
        exit

    else:
        print("Ugyldig valg")
        meny()

def normalmeny():
    print('''
        ****************************
        |1 Søk ettet vare
        |2 Se alle varer
        |3 Se varelogg
        |4 Avslutt
        ****************************            
          ''')
    
    valg2 = int(input("Velg en av alternativene ovenfor: "))

    if valg2 == 1:
        sookVare()

    elif valg2 == 2:
        seVarer()
    
    elif valg2 == 3:
        seVarelogg()
    
    elif valg2 == 4:
        exit
    
    else:
        print("Ugyldig valg")
        normalmeny()

def leggVare():
    nummer = random.randint(100000, 999999)
    navn = input("Skriv navnet på varen: ")
    kategori = input("Skriv kategori på varen: ")
    antall = input("Skriv antall varer: ")
    pris = input("Skriv prisen på varen(kr): ")
    vare1 = (nummer, navn, kategori, antall, pris)

    print(vare1)

    conn = get_db_connection()

    cursor = conn.cursor()
    cursor.execute("INSERT INTO varer (varenummer, navn, kategori, antall, pris) VALUES (%s,%s,%s,%s,%s)", vare1)
    conn.commit()
    cursor.execute("INSERT INTO varelogg (varenummer, endring) VALUES (%s,%s)", (vare1[0], "Legget til vare"))
    conn.commit()
    print("Varen ble lagt til!")
    meny()

def slettVare():

    slette = input("Skriv varenummer eller navn på varen du vil slette: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT varenummer FROM varer WHERE varenummer = %s OR navn = %s",(slette, slette))
    varenummer = cursor.fetchone()

    if varenummer is None:
        print("Varen finnes ikke")
    else:
        varenummer = varenummer[0]  
        cursor.execute("DELETE FROM varer WHERE varenummer = %s", (varenummer,))
        conn.commit()
        cursor.execute("INSERT INTO varelogg (varenummer, endring) VALUES (%s, %s)", (varenummer, "Slettet vare"))
        conn.commit()
        print("Varen ble slettet.")

    cursor.close() 
    conn.close()

    meny()

def sookVare():
    conn = get_db_connection()
    cursor = conn.cursor()
    valget = input("""Hva vil du søke etter?
                        |1 kategori
                        |2 varenummer/navn
                    """)

    if valget == "1":
        kategori = input("Skriv kategori du vil søke: ")
        cursor.execute("SELECT * FROM varer WHERE kategori = %s", (kategori,))
        conn.commit
        info = cursor.fetchall()
        
        if info is None:
            print("Det er ingen varer med denne kategorien")
        
        if info:
            colonne_navn = [desc[0] for desc in cursor.description]

            print(tabulate(info, headers=colonne_navn, tablefmt="grid"))
            input("Trykk enter for å gå tilbake til menyen")

            if brukernavn == "varelager" and passord == "123":
                meny()
            elif brukernavn == "varese" and passord == "321":
                normalmeny()

    
    elif valget == "2":
        navn = input("Skriv varenummer eller navn på varen du vil søke: ")
        cursor.execute("SELECT * FROM varer WHERE navn = %s OR varenummer = %s", (navn, navn))
        conn.commit
        info = cursor.fetchall()
        
        if info is None:
            print("Varen finnes ikke")
            
        
        if info:
            colonne_navn = [desc[0] for desc in cursor.description]

            print(tabulate(info, headers=colonne_navn, tablefmt="grid"))

        input("Trykk enter for å gå tilbake til menyen")

        if brukernavn == "varelager" and passord == "123":
                meny()
        elif brukernavn == "varese" and passord == "321":
            normalmeny()


def justerVare():
    conn = get_db_connection()
    cursor = conn.cursor()
    varen = input("Skriv varenummer eller navn på varen du vil justere: ")
    cursor.execute("SELECT varenummer FROM varer WHERE navn = %s OR varenummer = %s", (varen, varen))
    varetall = cursor.fetchone()
    if varetall is None:
        print("Varen finnes ikke")
        meny()
    if varetall:
        varetall = varetall[0]
    
    

        valget = input("""Hva ønsker du å justere?
                        |1 pris
                        |2 navn
                        |3 kategori
                        |4 antall
                        |5 Gå tilbake til meny
                    Velg en av alternativene ovenfor: """)
        if valget == "1":
            cursor.execute("Select pris FROM varer WHERE varenummer = %s OR navn = %s", (varen, varen))
            conn.commit()
            gammel_pris = cursor.fetchone()
            print("Gammel pris er: ", gammel_pris[0])
            ny_pris = float(input("Skriv ny pris: "))

            if ny_pris > 0 :
                cursor.execute("UPDATE varer SET pris = %s WHERE varenummer = %s OR navn = %s", (ny_pris, varen, varen))
                conn.commit()
                cursor.execute("INSERT INTO varelogg (varenummer, endring) VALUES (%s, %s)", (varetall, "Endret prisen på vare"))
                conn.commit()
                print("Prisen er nå justert")
            else:
                print("Prisen er ugyldig.")

            meny()
        
        elif valget == "2":
            cursor.execute("Select navn FROM varer WHERE varenummer = %s OR navn = %s", (varen, varen))
            gammel_navn = cursor.fetchone()
            print("Gammel navn er: ", gammel_navn[0])
            ny_navn = input("Skriv ny navn: ")

            if ny_navn != gammel_navn[0]:
                cursor.execute("UPDATE varer SET navn = %s WHERE varenummer = %s OR navn = %s", (ny_navn, varen, varen))
                conn.commit()
                cursor.execute("INSERT INTO varelogg (varenummer, endring) VALUES (%s, %s)", (varetall, "Endret navn på vare"))
                conn.commit()
            
            if ny_navn == gammel_navn[0]:
                print("Navnet er ugyldig.")
            
            meny()
        
        elif valget == "3":
            cursor.execute("Select kategori FROM varer WHERE varenummer = %s OR navn = %s", (varen, varen))
            gammel_kategori = cursor.fetchone()
            print("Gammel kategori er: ", gammel_kategori[0])
            ny_kategori = input("Skriv ny kategori: ")

            if ny_kategori != gammel_kategori[0]:
                cursor.execute("UPDATE varer SET kategori = %s WHERE varenummer = %s OR navn = %s", (ny_kategori, varen, varen))
                conn.commit()
                cursor.execute("INSERT INTO varelogg (varenummer, endring) VALUES (%s, %s)", (varetall, "Endret kategori på vare"))
                conn.commit()
            
            if ny_kategori == gammel_kategori[0]:
                print("Kategorien er ugyldig.")
            
            meny()

        elif valget == "4":
            cursor.execute("SELECT antall FROM varer WHERE varenummer = %s OR navn = %s", (varen, varen))
            gammel_antall = cursor.fetchone()
            print("Gammel antall er: ", gammel_antall[0])
            ny_antall = input("Skriv ny antall: ")

            if ny_antall != gammel_antall[0]:
                cursor.execute("UPDATE varer SET antall = %s WHERE varenummer = %s OR navn = %s", (ny_antall, varen, varen))
                conn.commit()
                cursor.execute("INSERT INTO varelogg (varenummer, endring) VALUES (%s, %s)", (varetall, "Endret antall på vare"))
                conn.commit()
            
            if ny_antall == gammel_antall[0]:
                print("Antallet er ugyldig.")
            
            meny()
        
        elif valget == "5":
            meny()
    
def seVarer():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM varer")
    conn.commit
    tabell = cursor.fetchall()

    colonne_navn = [desc[0] for desc in cursor.description]

    print(tabulate(tabell, headers=colonne_navn, tablefmt="grid"))
    input("Trykk enter for å gå tilbake til menyen")
    
    if brukernavn == "varelager" and passord == "123":
        meny()
    elif brukernavn == "varese" and passord == "321":
        normalmeny()

def seVarelogg():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM varelogg")
    conn.commit
    tabell = cursor.fetchall()

    colonne_navn = [desc[0] for desc in cursor.description]

    print(tabulate(tabell, headers=colonne_navn, tablefmt="grid"))
    input("Trykk enter for å gå tilbake til menyen")

    if brukernavn == "varelager" and passord == "123":
        meny()
    elif brukernavn == "varese" and passord == "321":
        normalmeny()


if brukernavn == "varelager" and passord == "123":
        meny()
elif brukernavn == "varese" and passord == "321":
    normalmeny()
else:
    print("Ugyldig brukernavn eller passord")

