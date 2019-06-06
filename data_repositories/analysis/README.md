# ChartCreator

main.ChartCreator
	-> main-Methode, definiert welche Diagramme geplottet werden sollen und wo die CSVs liegen
	-> enthält Methoden zum Erzeugen der Charts
	
charts -> Paket für die Ablage der verschiedenen Charttypen, im Moment zwei 
	-> BarChart für Anteil gefüllter Attribute (insgesamt oder pro Jahr) und
	-> LineChart für Datensätze pro Jahr
	-> in den Chartklassen können die Chart-Eigenschaften geändert werden
data -> Paket für Daten-bezogene Aspekte
	-> Category -> definiert unsere 14 Kategorien
	-> CategoryToColorMap -> definiert, welche Farbe für welche Kategorie verwendet werden soll
	-> TermToCategoryMap -> bildet Attributnamen (nur der Teil des Namens nach dem letzten Slash) auf unsere Kategorien ab
	-> RepositorySummary und DatasetSummary -> interne Datenstrukturen für die Daten aus den CSV-Files
		-> RepositorySummary -> Repository-Name, verfügbare Metadatenstandards und die eigentlichen Daten in einer DatasetSummary
		-> DatasetSummary -> speichert Datensatz-IDs, vorhandene Metadatenfelder, Datensatzdatum, Attributstatus (gesetzt/nicht gesetzt)

processors.io -> Paket für Datenprozessierungsaspekte
	-> RepositorySummaryReader -> Einlesen der CSV-Dateien in interne Datenstrukturen (RepositorySummary und DatasetSummary)
