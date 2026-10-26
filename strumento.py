class Strumento:
    """Rappresenta uno strumento musicale del deposito"""

    def __init__(self, codice, tipo, marca, anno_acquisto, valore, disponibile=True):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore
        self.disponibile = disponibile

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "In prestito"
        return (f"{self.codice}: {self.tipo} {self.marca} (acquistato nel {self.anno_acquisto}) "
                f"- valore {self.valore} euro - {stato}")

    def __repr__(self):
        stato = "Disponibile" if self.disponibile else "In prestito"
        return (f"{self.codice}: {self.tipo} {self.marca} (acquistato nel {self.anno_acquisto}) "
                f"- valore {self.valore} euro - {stato}")