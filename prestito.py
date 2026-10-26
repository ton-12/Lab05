class Prestito:
    """Rappresenta un prestito in corso di uno strumento"""

    def __init__(self, codice, data, id_strumento, cognome_allievo):
        self.codice = codice
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"{self.codice}: strumento {self.id_strumento} in prestito a {self.cognome_allievo} dal {self.data}"

    def __repr__(self):
        return f"{self.codice}: strumento {self.id_strumento} in prestito a {self.cognome_allievo} dal {self.data}"