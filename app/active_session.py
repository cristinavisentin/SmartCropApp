class StringCollection:
    def __init__(self):
        self.collection = []  # Usa una lista per la collezione

    def add(self, element):
        if element not in self.collection:
            self.collection.append(element)
            return f'"{element}" aggiunto alla collezione.'
        return f'"{element}" è già presente nella collezione.'

    def remove(self, element):
        if element in self.collection:
            self.collection.remove(element)
            return f'"{element}" rimosso dalla collezione.'
        return f'"{element}" non trovato nella collezione.'

    def contains(self, element):
        return element in self.collection

    def display(self):
        return self.collection
