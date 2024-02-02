# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
#   Imports
import argparse
import csv
import os
import random

import datetime as dt
from datetime import datetime, timedelta
from rich import print
from rich.table import Table


# Definieer paden en headers
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(MAIN_DIR, "data")
BOUGHT_FILE_PATH = os.path.join(DATA_DIR, "bought.csv")
SOLD_FILE_PATH = os.path.join(DATA_DIR, "sold.csv")

CURRENT_DATE_FILE_PATH = os.path.join(MAIN_DIR, "data/current_date.txt")

BOUGHT_CSV_HEADERS = ["ID", "Product Name", "Quantity", "Expiration Date", "Buy Price", "Buy Date"]
SOLD_CSV_HEADERS = ["ID", "Product Name", "Quantity", "Selling Price", "Selling Date"]

#   FUNCTIES VOOR HET AANMAKEN VAN FOLDERS EN BESTANDEN

def create_directory(directory_name):
    # Maak een directory als deze nog niet bestaat
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            print(f"Directory '{directory_name}' has been successfully created.")
    except Exception as e:
        print(f"[red]Error in creating the directory{directory_name}: {e}[/red]")

def create_csv_file(file_path, headers):
    # Maak een nieuw CSV-bestand met headers
    try:
        with open(file_path, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            print(f"File '{file_path}' has been successfully created and headers have been added.")
    except FileExistsError:
        pass
    except Exception as e:
        print(f"[red]Error writing to the file {file_path}: {e}[/red]")

def create_current_date_file(file_path):
    # Maak een nieuw bestand als het nog niet bestaat
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                print(f"File '{file_path}' has been successfully created.")
        else:
            pass
    except Exception as e:
        print(f"[red]Error writing to the file {file_path}: {e}[/red]")

def write_current_date(file_path):
    # Schrijf de huidige datum naar het bestand
    try:
        with open(file_path, 'w') as file:
            current_date = dt.date.today().strftime("%Y-%m-%d")
            file.write(current_date)
    except Exception as e:
        print(f"[red]Error writing to the file {file_path}: {e}[/red]")


create_directory(DATA_DIR)
create_csv_file(BOUGHT_FILE_PATH, BOUGHT_CSV_HEADERS)
create_csv_file(SOLD_FILE_PATH, SOLD_CSV_HEADERS)
create_current_date_file(CURRENT_DATE_FILE_PATH)
write_current_date(CURRENT_DATE_FILE_PATH)

#   VALIDATIES
def validate_and_convert_date(date_str):
    # Probeer de datum te converteren van het formaat 'YYYY-MM-DD'
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        # Als het eerste formaat faalt, probeer dan 'DD-MM-YYYY'
        try:
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            # Retourneer None als beide formaten falen
            return None

#   UTILS
def generate_id():
    # Genereert een unieke ID bestaande uit 6 willekeurige cijfers
    try:
        random_digits = [str(random.randint(0, 9)) for _ in range(6)]
        return ''.join(random_digits)
    except Exception as e:
        print(f"[red]Error while generating random digits: {e}")
        return None

def display_current_date(title="Date", date_changed=False):
    # Toont de huidige datum uit een bestand
    try:
        with open(CURRENT_DATE_FILE_PATH, 'r') as file:
            current_date_str = file.read().strip()
            current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()

        table = Table(title=title)
        table.add_column("Current Date", justify="left")
        table.add_row(str(current_date))

        # Toon een bericht als de datum is veranderd
        if date_changed:
            print("[green]The date has been successfully changed.[/green]")

        print(table)
    except Exception as e:
        print(f"[red]Error displaying date: {e}[/red]")

def advance_date(days):
    # Past de datum aan in het bestand op basis van het aantal opgegeven dagen
    try:
        days = int(days)
        with open(CURRENT_DATE_FILE_PATH, 'r') as file:
            current_date_str = file.read().strip()
            current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()

        new_date = current_date + timedelta(days=days)

        if days > 0:
            title = f"Date Advanced to {new_date}"
        elif days < 0:
            title = f"Date Set Back to {new_date}"
        else:
            title = "Current Date"

        with open(CURRENT_DATE_FILE_PATH, 'w') as file:
            file.write(new_date.strftime('%Y-%m-%d'))

        display_current_date(title, date_changed=True)
    except ValueError:
        print("[red]Invalid input for days. Please provide an integer.[/red]")
    except Exception as e:
        print(f"[red]Error advancing date: {e}[/red]")

#   CALCULATIONS
def calculate_stock(product_name):
    # Initialiseren van de gekochte en verkochte hoeveelheden
    bought_quantity = 0
    sold_quantity = 0

    try:
        # Open het bestand met gekochte producten en lees de inhoud
        with open(BOUGHT_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            # Bereken de totale gekochte hoeveelheid voor het opgegeven product
            for row in reader:
                if row["Product Name"] == product_name:
                    bought_quantity += int(row["Quantity"])
    except Exception as e:
        # Print een foutmelding als het bestand niet gelezen kan worden
        print(f"[red]Error reading {BOUGHT_FILE_PATH}: {e}")
        return None

    try:
        # Open het bestand met verkochte producten en lees de inhoud
        with open(SOLD_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            # Bereken de totale verkochte hoeveelheid voor het opgegeven product
            for row in reader:
                if row["Product Name"] == product_name:
                    sold_quantity += int(row["Quantity"])
    except Exception as e:
        # Print een foutmelding als het bestand niet gelezen kan worden
        print(f"[red]Error reading {SOLD_FILE_PATH}: {e}")
        return None

    return bought_quantity - sold_quantity

def calculate_report_for_date_range(start_date, end_date):
    # Bereken een voorraadrapport voor een bepaalde datumbereik
    try:
        current_date = start_date
        while current_date <= end_date:
            # print(f"\nInventory on {current_date}:")
            calculate_report_for_single_date(current_date, is_range=True)
            current_date += timedelta(days=1)
    except Exception as e:
        print(f"[red]Error while calculating inventory from {start_date} to {end_date}: {e}")

def calculate_report_for_single_date(target_date, is_range=False):
    # Bereken een voorraadrapport voor een enkele datum
    try:
        bought_inventory = {}
        sold_inventory = {}

        # Lees gekochte en verkochte voorraad uit bestanden
        with open(BOUGHT_FILE_PATH, 'r') as bought_file, open(SOLD_FILE_PATH, 'r') as sold_file:
            # Verwerken van gekochte voorraad
            reader = csv.DictReader(bought_file)
            for row in reader:
                buy_date = datetime.strptime(row['Buy Date'], '%Y-%m-%d').date()
                if buy_date <= target_date:
                    product_name = row['Product Name']
                    if product_name not in bought_inventory:
                        bought_inventory[product_name] = 0
                    bought_inventory[product_name] += int(row['Quantity'])

            # Verwerken van verkochte voorraad
            reader = csv.DictReader(sold_file)
            for row in reader:
                sell_date = datetime.strptime(row['Selling Date'], '%Y-%m-%d').date()
                if sell_date <= target_date:
                    product_name = row['Product Name']
                    if product_name not in sold_inventory:
                        sold_inventory[product_name] = 0
                    sold_inventory[product_name] += int(row['Quantity'])

        # Maak een tabel voor het voorraadrapport
        table = Table(title="Inventory Report" if is_range else f"Inventory on {target_date}")

        # Voeg kolommen toe aan de tabel
        table.add_column("Product Name", justify="left")
        table.add_column("Quantity Bought", justify="right")
        table.add_column("Quantity Sold", justify="right")
        table.add_column("Current Stock", justify="right")

        # Vul de tabel met voorraadgegevens
        for product in bought_inventory:
            bought_qty = bought_inventory[product]
            sold_qty = sold_inventory.get(product, 0)
            stock = bought_qty - sold_qty

            if stock > 0:
                table.add_row(
                    product,
                    str(bought_qty),
                    str(sold_qty),
                    str(stock)
                )

        print(table)

    except Exception as e:
        print(f"[red]Error calculating inventory on {target_date}: {e}[/red]")

def calculate_profit(start_date, end_date):
    # Bereken de totale winst over een datumbereik
    total_profit = 0.0
    try:
        current_date = start_date
        while current_date <= end_date:
            daily_profit = calculate_daily_profit(current_date)
            if daily_profit is not None:
                total_profit += daily_profit
            current_date += timedelta(days=1)
    except Exception as e:
        print(f"[red]Error calculating profit: {e}[/red]")
    return total_profit

def calculate_daily_profit(date):
    # Bereken de dagelijkse winst voor een specifieke datum
    try:
        daily_profit = 0.0
        # Lees verkochte voorraadgegevens
        with open(SOLD_FILE_PATH, 'r') as sold_file:
            sold_reader = csv.DictReader(sold_file)
            for sold_row in sold_reader:
                selling_date = datetime.strptime(sold_row['Selling Date'], '%Y-%m-%d').date()
                if selling_date == date:
                    product_name = sold_row['Product Name']
                    selling_price = float(sold_row['Selling Price'])
                    quantity_sold = int(sold_row['Quantity'])

                    # Bereken winst per verkocht item
                    with open(BOUGHT_FILE_PATH, 'r') as bought_file:
                        bought_reader = csv.DictReader(bought_file)
                        for bought_row in bought_reader:
                            if bought_row['Product Name'] == product_name:
                                buy_price = float(bought_row['Buy Price'])
                                profit_per_item = selling_price - buy_price
                                daily_profit += profit_per_item * quantity_sold
        return daily_profit
    except Exception as e:
        print(f"[red]Error calculating daily profit: {e}[/red]")
        return None

def calculate_revenue(start_date, end_date):
    # Bereken de totale omzet over een datumbereik
    total_revenue = 0.0
    try:
        # Lees verkochte voorraadgegevens
        with open(SOLD_FILE_PATH, 'r') as sold_file:
            sold_reader = csv.DictReader(sold_file)
            for row in sold_reader:
                selling_date = datetime.strptime(row['Selling Date'], '%Y-%m-%d').date()
                if start_date <= selling_date <= end_date:
                    selling_price = float(row['Selling Price'])
                    quantity_sold = int(row['Quantity'])
                    total_revenue += selling_price * quantity_sold
    except Exception as e:
        print(f"[red]Error while calculating revenue: {e}[/red]")
    return total_revenue

#   REPORTS: INVENTORY
def inventory_report(today, yesterday, date_arg, start_date, end_date):
    # Bereken een voorraadrapport voor een specifieke datum of datumbereik.
    try:
        # Rapport voor vandaag.
        if today:
            target_date = datetime.today().date()
            calculate_report_for_single_date(target_date)
        # Rapport voor gisteren.
        elif yesterday:
            target_date = datetime.today().date() - timedelta(days=1)
            calculate_report_for_single_date(target_date)
        # Rapport voor een specifieke datum.
        elif date_arg:
            validated_date = validate_and_convert_date(date_arg)
            if validated_date is None:
                raise ValueError("Invalid date format for 'date'")
            target_date = datetime.strptime(validated_date, '%Y-%m-%d').date()
            calculate_report_for_single_date(target_date)
        # Rapport voor een datumbereik.
        elif start_date and end_date:
            validated_start_date = validate_and_convert_date(start_date)
            validated_end_date = validate_and_convert_date(end_date)
            if validated_start_date is None or validated_end_date is None:
                raise ValueError("Invalid date format for 'start_date' or 'end_date'")
            start_date = datetime.strptime(validated_start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(validated_end_date, '%Y-%m-%d').date()
            calculate_report_for_date_range(start_date, end_date)
        else:
            raise ValueError("No valid date parameter specified")
    except ValueError as ve:
        print(f"Date validation error: {ve}")
    except Exception as e:
        print(f"General error: {e}")

#   REPORTS: PROFIT
def profit_report(today, yesterday, date_arg, start_date, end_date):
    # Genereert een winstrapport voor een bepaalde dag of periode.
    try:
        table = Table(title="Profit Report")
        table.add_column("Date", justify="left")
        table.add_column("Profit", justify="right")

        # Behandelt vandaag, gisteren of een specifieke datum.
        if today or yesterday or date_arg:
            if today:
                target_date = datetime.today().date()
            elif yesterday:
                target_date = datetime.today().date() - timedelta(days=1)
            elif date_arg:
                validated_date = validate_and_convert_date(date_arg)
                if validated_date is None:
                    raise ValueError("Invalid date format for 'date'")
                target_date = datetime.strptime(validated_date, '%Y-%m-%d').date()

            daily_profit = calculate_profit(target_date, target_date)
            table.add_row(str(target_date), f"{daily_profit:.2f}")
        # Behandelt een datumbereik.
        elif start_date and end_date:
            validated_start_date = validate_and_convert_date(start_date)
            validated_end_date = validate_and_convert_date(end_date)
            if validated_start_date is None or validated_end_date is None:
                raise ValueError("Invalid date format for 'start_date' or 'end_date'")
            start_date = datetime.strptime(validated_start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(validated_end_date, '%Y-%m-%d').date()
            total_profit = calculate_profit(start_date, end_date)
            table.add_row(f"{start_date} to {end_date}", f"{total_profit:.2f}")

        print(table)
    except ValueError as ve:
        print(f"Date validation error: {ve}")
    except Exception as e:
        print(f"General error: {e}")

#   REPORTS: REVENUE
def revenue_report(today, yesterday, date_arg, start_date, end_date):
    # Creëert een omzetrapport voor een specifieke dag of periode.
    try:
        table = Table(title="Revenue Report")
        table.add_column("Date", justify="left")
        table.add_column("Revenue", justify="right")

        # Behandelt vandaag, gisteren of een specifieke datum.
        if today or yesterday or date_arg:
            if today:
                target_date = datetime.today().date()
            elif yesterday:
                target_date = datetime.today().date() - timedelta(days=1)
            elif date_arg:
                validated_date = validate_and_convert_date(date_arg)
                if validated_date is None:
                    raise ValueError("Invalid date format for 'date'")
                target_date = datetime.strptime(validated_date, '%Y-%m-%d').date()

            daily_revenue = calculate_revenue(target_date, target_date)
            table.add_row(str(target_date), f"{daily_revenue:.2f}")

        # Behandelt een datumbereik.
        elif start_date and end_date:
            validated_start_date = validate_and_convert_date(start_date)
            validated_end_date = validate_and_convert_date(end_date)
            if validated_start_date is None or validated_end_date is None:
                raise ValueError("Invalid date format for 'start_date' or 'end_date'")
            start_date_obj = datetime.strptime(validated_start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(validated_end_date, '%Y-%m-%d').date()
            total_revenue = calculate_revenue(start_date_obj, end_date_obj)
            table.add_row(f"{start_date_obj} to {end_date_obj}", f"{total_revenue:.2f}")

        print(table)
    except ValueError as ve:
        print(f"Date validation error: {ve}")
    except Exception as e:
        print(f"General error: {e}")

#   REPORTS: EXPIRATION DATE
def expiration_report():
    # Genereert een rapport van producten die binnen 2 weken verlopen
    try:
        # Leest de huidige datum uit een bestand
        with open(CURRENT_DATE_FILE_PATH, 'r') as file:
            current_date_str = file.read().strip()
            current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()

        expiring_products = []

        # Verzamelt producten die binnen 14 dagen verlopen
        with open(BOUGHT_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expiration_date = datetime.strptime(row['Expiration Date'], '%Y-%m-%d').date()
                if expiration_date <= current_date + timedelta(days=14):
                    expiring_products.append(row)

        # Sorteert producten op vervaldatum
        expiring_products.sort(key=lambda x: datetime.strptime(x['Expiration Date'], '%Y-%m-%d').date())

        # Maakt een tabel met verlopende producten
        table = Table(title="Products Expiring Within 2 Weeks")

        table.add_column("Product Name", justify="left")
        table.add_column("Expiration Date", justify="right")

        for product in expiring_products:
            table.add_row(
                product['Product Name'],
                product['Expiration Date']
            )

        print(table)

    except Exception as e:
        print(f"[red]Error generating expiration list report: {e}[/red]")

# FILTER
def filter_inventory(field, value):
    # Filtert de voorraad op een bepaald veld en waarde
    try:
        # Controleert of het veld geldig is
        if field not in BOUGHT_CSV_HEADERS:
            raise ValueError(f"Field '{field}' is not valid. Choose from {BOUGHT_CSV_HEADERS}")

        filtered_results = []
        with open(BOUGHT_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            filtered_results = [row for row in reader if row[field] == value]

        # Toont gefilterde resultaten of een melding als er geen zijn
        if not filtered_results:
            print(f"No results found for {field} = {value}.")
        else:
            table = Table(title=f"Filtered Results for {field} = {value}")

            for header in BOUGHT_CSV_HEADERS:
                table.add_column(header, justify="left")

            for result in filtered_results:
                table.add_row(*[result[header] for header in BOUGHT_CSV_HEADERS])

            print(table)

    except ValueError as ve:
        print(f"[red]Error: {ve}[/red]")
    except Exception as e:
        print(f"[red]Unexpected error: {e}[/red]")

#   SEARCH
def search_inventory(field, term):
    # Zoekt in de voorraad op een bepaald veld met een zoekterm
    try:
        # Controleert of het veld geldig is
        if field not in BOUGHT_CSV_HEADERS:
            raise ValueError(f"Field '{field}' is not valid. Choose from {BOUGHT_CSV_HEADERS}")

        with open(BOUGHT_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            filtered_results = [row for row in reader if term.lower() in row[field].lower()]

        # Toont zoekresultaten of een melding als er geen zijn
        if not filtered_results:
            print(f"No results found for {term} in {field}.")
        else:
            table = Table(title=f"Search Results for '{term}' in '{field}'")
            
            for header in BOUGHT_CSV_HEADERS:
                table.add_column(header, justify="left")

            for result in filtered_results:
                table.add_row(*[result[header] for header in BOUGHT_CSV_HEADERS])

            print(table)

    except Exception as e:
        print(f"[red]Error searching inventory: {e}[/red]")

    except Exception as e:
        print(f"[red]Error searching inventory: {e}[/red]")

#   SORT
def sort_inventory(field, order):
    # Sorteert de voorraad op een bepaald veld in oplopende of aflopende volgorde
    try:
        # Controleert of het veld geldig is
        if field not in BOUGHT_CSV_HEADERS:
            raise ValueError(f"Field '{field}' is not valid. Choose from {BOUGHT_CSV_HEADERS}")

        with open(BOUGHT_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            sorted_results = sorted(reader, key=lambda row: row[field], reverse=(order == 'desc'))

         # Toont gesorteerde resultaten of een melding als er geen zijn
        if not sorted_results:
            print(f"No results to sort on {field}.")
        else:
            table = Table(title=f"Sorted results on {field} ({order})")
            
            for header in BOUGHT_CSV_HEADERS:
                table.add_column(header, justify="left")

            for result in sorted_results:
                table.add_row(*[result[header] for header in BOUGHT_CSV_HEADERS])

            print(table)

    except Exception as e:
        print(f"[red]Error sorting inventory: {e}[/red]")

# BUY
def buy_product(product_name, quantity, buy_price, expiration_date):
    # Probeer de opgegeven hoeveelheid om te zetten naar een geheel getal
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        print("Quantity must be an integer greater than 0.")
        return

    # Probeer de opgegeven aankoopprijs om te zetten naar een getal
    try:
        buy_price = float(buy_price)
        if buy_price < 0:
            raise ValueError
    except ValueError:
        print("Buy price must be a positive number.")
        return

    # Probeer de huidige datum op te halen uit een bestand
    try:
        with open(CURRENT_DATE_FILE_PATH, 'r') as file:
            buy_date = file.read().strip()
    except Exception as e:
        print(f"[red]Error retrieving the current date: {e}")
        return

    # Valideer en converteer de opgegeven vervaldatum
    converted_date = validate_and_convert_date(expiration_date)
    if not converted_date:
        print("Invalid expiration date.")
        return

    # Genereer een unieke ID voor het product
    product_id = generate_id()

    # Voeg de aankoop toe aan het aankoopbestand
    try:
        with open(BOUGHT_FILE_PATH, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product_id, product_name, quantity, converted_date, buy_price, buy_date])
            print(f"Purchase of {product_name} has been successfully added.")
    except Exception as e:
        print(f"[red]Error adding the purchase: {e}[/red]")


#   SELL
def sell_product(product_name, quantity, selling_price):
    # Probeer de opgegeven hoeveelheid om te zetten naar een geheel getal
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        print("Quantity must be an integer and greater than 0.")
        return

    # Probeer de opgegeven verkoopprijs om te zetten naar een getal
    try:
        selling_price = float(selling_price)
        if selling_price < 0:
            raise ValueError
    except ValueError:
        print("Selling price must be a positive number.")
        return

    # Bereken de huidige voorraad van het product
    current_stock = calculate_stock(product_name)
    if current_stock is None:
        print("Unable to calculate current stock.")
        return

    # Controleer of er voldoende voorraad is om te verkopen
    if quantity > current_stock:
        print(f"There are not enough {product_name} in stock. Available quantity: {current_stock}")
        return

    # Probeer de huidige datum op te halen uit een bestand
    try:
        with open(CURRENT_DATE_FILE_PATH, 'r') as file:
            selling_date = file.read().strip()
    except Exception as e:
        print(f"[red]Error while fetching the current date: {e}")
        return

    # Genereer een unieke ID voor het product
    product_id = generate_id()

    # Voeg de verkoop toe aan het verkoopbestand
    try:
        with open(SOLD_FILE_PATH, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product_id, product_name, quantity, selling_price, selling_date])
            print(f"Selling of {product_name} has been successfully added.")
    except Exception as e:
        print(f"[red]Error while adding the sale: {e}[/red]")

#   PARSERS
def parsers():
    #   Hoofdparser
    parser = argparse.ArgumentParser(
        description="SuperPy - A tool for an supermarket inventory management system")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands for managing inventory, sales, and reporting")

    #   Commando's voor de subparser 'buy'
    buy_parser = subparsers.add_parser("buy", help="Register a new purchase")
    buy_parser.add_argument("--product-name", help="Name of the product being bought")
    buy_parser.add_argument("--quantity", type=int, help="Quantity of the product being bought")
    buy_parser.add_argument("--price", type=float, help="Price of the product")
    buy_parser.add_argument("--expiration-date", help="Expiration date of the product (format: YYYY-MM-DD)")

    #   Commando's voor de subparser 'sell'
    sell_parser = subparsers.add_parser("sell", help="Register a new sale")
    sell_parser.add_argument("--product-name", help="Name of the product being sold")
    sell_parser.add_argument("--quantity", type=int, help="Quantity of the product being sold")
    sell_parser.add_argument("--price", type=float, help="Selling price of the product")

    #   Commando's voor de subparser 'report'
    report_parser = subparsers.add_parser(
        "report", help="Generate different types of reports")
    report_subparsers = report_parser.add_subparsers(dest="command_report")

    #   Commando's voor de report subparser 'inventory'
    inventory_subparser = report_subparsers.add_parser("inventory", help="Report current inventory")
    inventory_subparser.add_argument("--today", action="store_true", help="Show inventory for today")
    inventory_subparser.add_argument("--yesterday", action="store_true", help="Show inventory for yesterday")
    inventory_subparser.add_argument("--date", help="Show inventory for a specific date (format: YYYY-MM-DD)")
    inventory_subparser.add_argument("--start-date", help="Start date for the inventory report (format: YYYY-MM-DD)")
    inventory_subparser.add_argument("--end-date", help="End date for the inventory report (format: YYYY-MM-DD)")

    #   Commando's voor de report subparser 'profit'
    profit_subparser = report_subparsers.add_parser("profit", help="Report profits")
    profit_subparser.add_argument("--today", action="store_true", help="Show profit for today")
    profit_subparser.add_argument("--yesterday", action="store_true", help="Show profit for yesterday")
    profit_subparser.add_argument("--date", help="Show profit for a specific date (format: YYYY-MM-DD)")
    profit_subparser.add_argument("--start-date", help="Start date for the profit report (format: YYYY-MM-DD)")
    profit_subparser.add_argument("--end-date", help="End date for the profit report (format: YYYY-MM-DD)")

    #   Commando's voor de report subparser 'revenue'
    revenue_subparser = report_subparsers.add_parser("revenue", help="Report revenue")
    revenue_subparser.add_argument("--today", action="store_true", help="Show revenue for today")
    revenue_subparser.add_argument("--yesterday", action="store_true", help="Show revenue for yesterday")
    revenue_subparser.add_argument("--date", help="Show revenue for a specific date (format: YYYY-MM-DD)")
    revenue_subparser.add_argument("--start-date", help="Start date for the revenue report (format: YYYY-MM-DD)")
    revenue_subparser.add_argument("--end-date", help="End date for the revenue report (format: YYYY-MM-DD)")

    expiration_report_subparser = report_subparsers.add_parser("expiration", help="Report products expiring within 2 weeks")
    expiration_report_subparser.add_argument("--list", action="store_true", help="List products expiring within 2 weeks")
    
    #   Commando's voor de subparser 'filter'
    filter_parser = subparsers.add_parser("filter", help="Filter inventory items")
    filter_parser.add_argument("--field", help="Field to filter by", choices=BOUGHT_CSV_HEADERS)
    filter_parser.add_argument("--value", help="Value to filter for")

    #   Commando's voor de subparser 'search'
    search_parser = subparsers.add_parser("search", help="Search inventory items")
    search_parser.add_argument("--field", help="Field to search in", choices=BOUGHT_CSV_HEADERS)
    search_parser.add_argument("--term", help="Search term")

#   Commando's voor de subparser 'sort'
    sort_parser = subparsers.add_parser("sort", help="Sort inventory")
    sort_parser.add_argument("--field", choices=["Product Name", "Quantity", "Buy Price", "Expiration Date", "Buy Date"], help="Field to sort by")
    sort_parser.add_argument("--order", choices=['asc', 'desc'], default='asc', help="Sort order (ascending or descending)")

    #   Commando voor de parser voor 'advance-date'
    parser.add_argument("--current-date", action="store_true", help="Display the current date")
    parser.add_argument("--advance-date", type=int, help="Advance the current date by a specified number of days")

    return parser.parse_args()


def main():
    # Argumenten parseren
    args = parsers()

    # Product kopen
    if args.command == "buy":
        buy_product(args.product_name, args.quantity, args.price, args.expiration_date)
    
    # Product verkopen
    elif args.command == "sell":
        sell_product(args.product_name, args.quantity, args.price)

    # Rapporten genereren
    elif args.command == "report":
        # Inventarisrapport
        if args.command_report == "inventory":
            inventory_report(today=args.today,
                             yesterday=args.yesterday,
                             date_arg=args.date,
                             start_date=args.start_date,
                             end_date=args.end_date)
            
        # Winst rapport
        elif args.command_report == "profit":
            profit_report(today=args.today,
                          yesterday=args.yesterday,
                          date_arg=args.date,
                          start_date=args.start_date,
                          end_date=args.end_date)
            
        # Omzetrapport
        elif args.command_report == "revenue":
            revenue_report(today=args.today,
                           yesterday=args.yesterday,
                           date_arg=args.date,
                           start_date=args.start_date,
                           end_date=args.end_date)
            
        # Vervalrapport
        elif args.command_report == "expiration":
            if args.list:
                expiration_report()

    # Inventaris filteren
    elif args.command == "filter":
        filter_inventory(args.field, args.value)

    # Zoeken in inventaris
    elif args.command == "search":
        search_inventory(args.field, args.term)
    
    # Inventaris sorteren
    elif args.command == "sort":
        sort_inventory(field=args.field, order=args.order)
    
    # Huidige datum weergeven
    elif args.current_date:
        display_current_date()
    
    # Datum vooruitzetten
    elif args.advance_date is not None:
        advance_date(args.advance_date)

if __name__ == "__main__":
    main()