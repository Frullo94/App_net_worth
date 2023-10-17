import os
import csv
import matplotlib.pyplot as plt 
from datetime import datetime

# modifica esempio 2
FILE_NAME = "patrimonio.csv"

print("CIAO DA DAVIDE")

CATEGORIES = {
    "LIQUIDITÀ": {
        "Conto Corrente Intesa San Paolo": 0,
        "Superflash Intesa San Paolo": 0,
        "Saldo Paypal": 0,
        "Saldo Wise": 0,
        "Contanti": 0
    },
    "INVESTIMENTI FINANZIARI": {
        "Portafoglio Azioni Degiro": 0,
        "Liquidità Degiro": 0,
        "Portafoglio Azioni Interactive Brokers": 0,
        "Liquidità Interactive Brokers": 0,
        "Portafoglio Kraken": 0
    },
    "ASSET ALTERNATIVI": {
        "Vino": 0,
        "Arte": 0,
        "Vinili": 0
    },
    "PARTECIPAZIONI AZIENDALI": {
        "Birrificio 620 Passi": 0
    }
}

def ask_input(category):
    data = {}
    for item in CATEGORIES[category]:
        value = float(input(f"Enter {item}: "))
        data[item] = value
    return data

def add_element(category):
    new_item = input("Enter the name of the new item: ")
    value = float(input(f"Enter the value for {new_item}: "))  # modificare da qui
    CATEGORIES[category][new_item] = 0

def delete_element(category):
    print("Current items:")
    for item in CATEGORIES[category]:
        print(f"- {item}")
    item_to_delete = input("Enter the name of the item to delete: ")
    if item_to_delete in CATEGORIES[category]:
        del CATEGORIES[category][item_to_delete]
        print(f"'{item_to_delete}' successfully deleted!")
    else:
        print(f"'{item_to_delete}' not found.")

def save_data(data_to_save):
    today = datetime.now().strftime('%Y-%m-%d')

    # Se il file non esiste, creiamo l'intestazione
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w', newline='') as file:
            writer = csv.writer(file)
            header = ["Voce"]
            writer.writerow(header)
            for category in CATEGORIES:
                writer.writerow([category])
                for item in CATEGORIES[category]:
                    writer.writerow([item])

    # Leggiamo l'intero file in memoria
    with open(FILE_NAME, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Troviamo la colonna corrispondente alla data odierna o aggiungiamone una nuova
    if today not in rows[0]:
        for row in rows:
            row.append('')  # Aggiungiamo una cella vuota per la nuova data
        rows[0].append(today)

    today_col = rows[0].index(today)

    # Aggiorniamo i dati
    for row in rows[1:]:
        item_name = row[0]
        if item_name in data_to_save:
            while len(row) <= today_col:  # Assicuriamoci che la riga abbia abbastanza colonne
                row.append('')
            row[today_col] = data_to_save[item_name]

    # Sovrascriviamo il file con i dati aggiornati
    with open(FILE_NAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def modify_value(category):
    # Leggi il file CSV
    with open(FILE_NAME, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        header = rows[0]
        data = rows[1:]

    # Trova l'indice della voce selezionata
    index = header.index(category)

    # Mostra all'utente tutte le date in cui ha inserito un valore per quella voce
    print(f"Valori inseriti per {category}:")
    for row in data:
        print(f"Data: {row[0]}, Valore: {row[index]}")

    # Chiedi all'utente quale data desidera modificare
    date_to_modify = input("Inserisci la data che desideri modificare (YYYY-MM-DD): ")

    # Trova la riga con quella data
    for row in data:
        if row[0] == date_to_modify:
            # Chiedi all'utente il nuovo valore
            new_value = input(f"Inserisci il nuovo valore per {category} alla data {date_to_modify}: ")
            row[index] = new_value
            break

    # Sovrascrivi il file CSV con i nuovi dati
    with open(FILE_NAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    print(f"Valore per {category} alla data {date_to_modify} modificato con successo!")

def main():
    temp_data ={}
    while True:
        print("\nMenu:")
        print("1. Enter data for LIQUIDITÀ")
        print("2. Enter data for INVESTIMENTI FINANZIARI")
        print("3. Enter data for ASSET ALTERNATIVI")
        print("4. Enter data for PARTECIPAZIONI AZIENDALI")
        print("5. Add item to LIQUIDITÀ")
        print("6. Add item to INVESTIMENTI FINANZIARI")
        print("7. Add item to ASSET ALTERNATIVI")
        print("8. Add item to PARTECIPAZIONI AZIENDALI")
        print("9. Delete item from LIQUIDITÀ")
        print("10. Delete item from INVESTIMENTI FINANZIARI")
        print("11. Delete item from ASSET ALTERNATIVI")
        print("12. Delete item from PARTECIPAZIONI AZIENDALI")
        print("13. Modify value for LIQUIDITÀ")
        print("14. Modify value for INVESTIMENTI FINANZIARI")
        print("15. Modify value for ASSET ALTERNATIVI")
        print("16. Modify value for PARTECIPAZIONI AZIENDALI")
        print("18. Exit")
        choice = int(input("Choose an option: "))

        if 1 <= choice <= len(CATEGORIES):
            selected_category = list(CATEGORIES.keys())[choice - 1]
            temp_data.update(ask_input(selected_category))
            save_data(temp_data)
        elif len(CATEGORIES) < choice <= 2*len(CATEGORIES):
            selected_category = list(CATEGORIES.keys())[choice - len(CATEGORIES) - 1]
            add_element(selected_category)
        elif 2*len(CATEGORIES) < choice <= 3*len(CATEGORIES):
            selected_category = list(CATEGORIES.keys())[choice - 2*len(CATEGORIES) - 1]
            delete_element(selected_category)
        elif 3*len(CATEGORIES) < choice <= 4*len(CATEGORIES):
            selected_category = list(CATEGORIES.keys())[choice - 3*len(CATEGORIES) - 1]
            modify_value(selected_category)
        elif choice == 4*len(CATEGORIES) + 2:
            save_data(temp_data)
            break

if __name__ == "__main__":
    main()
