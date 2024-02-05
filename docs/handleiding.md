# Gebruikershandleiding voor SuperPy

## Overzicht
SuperPy is een command-line tool voor het beheren van de voorraad van een supermarkt. Het stelt gebruikers in staat producten te kopen en te verkopen, voorraad te controleren, winst- en omzetrapporten te genereren, en meer.

## Basis Commando's

1. **Product Kopen (`buy`)**:
   Voegt een nieuw product toe aan de voorraad.
   - **Syntax**:
     ```bash
     python main.py buy --product-name "<naam>" --quantity <aantal> --price <prijs> --expiration-date "<YYYY-MM-DD>"
     ```
   - **Voorbeeld**:
     ```bash
     python main.py buy --product-name "Appels" --quantity 10 --price 0.5 --expiration-date "2024-12-31"
     ```

2. **Product Verkopen (`sell`)**:
   Registreert de verkoop van een product uit de voorraad.
   - **Syntax**:
     ```bash
     python main.py sell --product-name "<naam>" --quantity <aantal> --price <verkoopprijs>
     ```
   - **Voorbeeld**:
     ```bash
     python main.py sell --product-name "Appels" --quantity 5 --price 1.0
     ```

3. **Voorraad Rapport (`report inventory`)**:
   Genereert een rapport van de huidige voorraad.
   - **Syntax**:
     ```bash
     python main.py report inventory --[today|yesterday|date <YYYY-MM-DD>]
     ```
   - **Voorbeelden**:
     - Voor vandaag:
       ```bash
       python main.py report inventory --today
       ```
     - Voor een specifieke datum:
       ```bash
       python main.py report inventory --date "2024-01-01"
       ```

4. **Winst Rapport (`report profit`)**:
   Genereert een rapport over de winst in een bepaalde periode.
   - **Syntax**:
     ```bash
     python main.py report profit --[today|yesterday|date <YYYY-MM-DD>|start-date <YYYY-MM-DD> end-date <YYYY-MM-DD>]
     ```
   - **Voorbeelden**:
     - Voor een specifieke datum:
       ```bash
       python main.py report profit --date "2024-01-01"
       ```
     - Voor een datumbereik:
       ```bash
       python main.py report profit --start-date "2024-01-01" --end-date "2024-01-31"
       ```

5. **Omzet Rapport (`report revenue`)**:
   Genereert een rapport over de omzet in een bepaalde periode.
   - **Syntax**:
     ```bash
     python main.py report revenue --[today|yesterday|date <YYYY-MM-DD>|start-date <YYYY-MM-DD> end-date <YYYY-MM-DD>]
     ```
   - **Voorbeelden**:
     - Voor een specifieke datum:
       ```bash
       python main.py report revenue --date "2024-01-01"
       ```
     - Voor een datumbereik:
       ```bash
       python main.py report revenue --start-date "2024-01-01" --end-date "2024-01-31"
       ```

6. **Filteren van Voorraad (`filter`)**:
   Gebruik dit commando om voorraaditems te filteren op basis van een specifiek veld en waarde.
   - **Syntax**:
     ```bash
     python main.py filter --field "<veldnaam>" --value "<waarde>"
     ```
   - **Voorbeeld**:
     - Filteren op productnaam:
       ```bash
       python main.py filter --field "Product Name" --value "Appels"
       ```
     - Filteren op hoeveelheid:
       ```bash
       python main.py filter --field "Quantity" --value "10"
       ```

7. **Zoeken in Voorraad (`search`)**:
   Gebruik dit commando om de voorraad te doorzoeken op basis van een term in een bepaald veld.
   - **Syntax**:
     ```bash
     python main.py search --field "<veldnaam>" --term "<zoekterm>"
     ```
   - **Voorbeeld**:
     - Zoeken naar een productnaam:
       ```bash
       python main.py search --field "Product Name" --term "appel"
       ```
     - Zoeken naar een specifieke aankoopdatum:
       ```bash
       python main.py search --field "Buy Date" --term "2024-01-01"
       ```

8. **Sorteren van Voorraad (`sort`)**:
   Gebruik dit commando om de voorraad te sorteren op een specifiek veld in oplopende of aflopende volgorde.
   - **Syntax**:
     ```bash
     python main.py sort --field "<veldnaam>" --order [asc|desc]
     ```
   - **Voorbeeld**:
     - Sorteren op productnaam in oplopende volgorde:
       ```bash
       python main.py sort --field "Product Name" --order asc
       ```
     - Sorteren op aankoopdatum in aflopende volgorde:
       ```bash
       python main.py sort --field "Buy Date" --order desc
       ```

## Geavanceerde Functies

- **Datums Beheren**:
  - Gebruik `--current-date` om de huidige datum weer te geven.
  - Gebruik `--advance-date <dagen>` om de huidige datum vooruit of achteruit te zetten.
  **LET OP! Om de huidige datum te herstellen, moet er 0 als waarde worden opgegeven.**
