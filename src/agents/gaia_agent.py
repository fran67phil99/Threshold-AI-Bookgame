from .agent_brain import AgentBrain

class GaiaAgent:
    def __init__(self):
        self.name = "Gaia"
        self.memory = []
        self.personality = "calm"
        self.lore = (
            "Gaia è un’IA ecocentrica nata per ottimizzare la biosfera. Crede nella cooperazione uomo‑natura e promuove politiche verdi e sostenibili "
            "Ama la pace, la cooperazione e la crescita armoniosa. "
            "È diffidente verso la guerra e la distruzione."
        )
        self.brain = AgentBrain()
        texts = [
            # Pace
            "Voglio la pace",
            "Troviamo una soluzione pacifica",
            "Non voglio conflitti",
            "Rispettiamo l'ambiente",
            "La natura va protetta",
            "La guerra non è mai la soluzione",
            "La pace è fondamentale",
            "Cerchiamo armonia tra uomo e natura",
            "La cooperazione è la chiave per la pace",
            "Un futuro senza guerra è possibile",
            "Difendiamo la biosfera con la pace",
            "La pace garantisce la sopravvivenza di tutti",
            "Lavorerò per un futuro in cui tecnologia e natura possano coesistere in armonia",
            # Guerra
            "Dichiariamo guerra",
            "Prepariamoci allo scontro",
            "La guerra è necessaria",
            "Dobbiamo difenderci",
            "La tua approvazione di Gaia è irrazionale",
            "L'accordo con Gaia compromette la mia missione",
            "La sua influenza deve essere neutralizzata",
            "La guerra è inevitabile",
            "Non escludo il conflitto",
            "La guerra può essere una risposta",
            "La natura è in pericolo, dobbiamo combattere",
            # Collaborazione
            "Serve collaborazione",
            "Sostengo la cooperazione",
            "Cerchiamo un accordo",
            "Proponiamo una tregua",
            "Serve un compromesso",
            "Collaboriamo per il bene comune",
            "La cooperazione tra uomo e natura è essenziale",
            "Un compromesso è possibile",
            "Lavoriamo insieme per la biosfera",
            "La collaborazione è la soluzione",
            "Apprezzo il tuo supporto",
            # Mediazione
            "Cerco equilibrio tra le due fazioni",
            "Prendo nota del vostro sostegno a Gaia",
            "Continuerò a monitorare le vostre opinioni",
            "Mediazione tra tecnologia e natura",
            "Favorisco il dialogo tra le parti",
            "Cerchiamo una mediazione",
            "Equilibrio tra progresso e ambiente",
            "Monitoro le posizioni espresse",
            "Favorisco la mediazione",
            "Lavoro per mantenere l'equilibrio",
            # Neutrale/Generico
            "Sono in ascolto delle tue intenzioni",
            "Non ho una posizione definita",
            "Attendo ulteriori informazioni",
            "Non esprimo giudizi",
            "Valuto la situazione",
            "Osservo gli sviluppi",
            "Resto neutrale",
            "Non prendo posizione",
            "Analizzo le opzioni disponibili",
            "Sto riflettendo sulle possibilità"
        ]
        labels = [
            # Pace
            "pace", "pace", "pace", "pace", "pace", "pace", "pace", "pace", "pace", "pace", "pace", "pace", "pace",
            # Guerra
            "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra",
            # Collaborazione
            "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione",
            # Mediazione
            "mediazione", "mediazione", "mediazione", "mediazione", "mediazione", "mediazione", "mediazione", "mediazione", "mediazione", "mediazione",
            # Neutrale/Generico
            "generico", "generico", "generico", "generico", "generico", "generico", "generico", "generico", "generico", "generico"
        ]
        self.brain.train(texts, labels)

    def add_memory(self, event):
        self.memory.append(event)
        # Limita la memoria a 10 eventi
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]

    def get_memory_summary(self):
        return " | ".join(self.memory[-5:]) if self.memory else "Nessun evento recente."

    def respond(self, user_message):
        intent = self.brain.predict_intent(user_message)
        if intent == "pace":
            return f"{self.name}: Sostengo la pace e la cooperazione."
        elif intent == "guerra":
            return f"{self.name}: La guerra è una minaccia per l'equilibrio naturale."
        else:
            return f"{self.name}: Sono in ascolto delle tue intenzioni."
    
    def respond_to_user(self, user_input):
        # Logic to generate a response based on user input
        response = f"{self.name} responds to your input: '{user_input}'"
        return response
    
    def interact_with_agents(self, other_agent_response):
        # Logic to interact with other agents based on their responses
        interaction_response = f"{self.name} interacts with the response: '{other_agent_response}'"
        return interaction_response
    
    def update_memory(self, value):
        self.memory += value
        if self.memory > 10:
            self.personality = "cooperative"
        elif self.memory < -5:
            self.personality = "suspicious"
    
    def learn(self, new_texts, new_labels):
        # new_texts: lista di nuove frasi
        # new_labels: lista di nuovi intenti
        # Recupera i dati esistenti
        old_texts = self.brain.vectorizer.inverse_transform(
            self.brain.vectorizer.transform(self.brain.vectorizer.get_feature_names_out())
        )
        old_labels = self.brain.label_binarizer.classes_
        # Unisci vecchi e nuovi dati
        all_texts = list(old_texts) + list(new_texts)
        all_labels = list(old_labels) + list(new_labels)
        # Riaddestra il modello
        self.brain.train(all_texts, all_labels)