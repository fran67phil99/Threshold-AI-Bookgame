import json
import os

class LoreComune:
    def __init__(self, filepath="src/data/lore_comune.json"):
        self.filepath = filepath
        self.eventi = []
        self.carica_da_file()

    def aggiungi_evento(self, evento):
        self.eventi.append(evento)
        self.salva_su_file()

    def get_lore(self, max_eventi=10):
        if not self.eventi:
            return "Nessun evento importante è ancora accaduto."
        return " | ".join(self.eventi[-max_eventi:])

    def salva_su_file(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.eventi, f, ensure_ascii=False, indent=2)

    def carica_da_file(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.eventi = json.load(f)