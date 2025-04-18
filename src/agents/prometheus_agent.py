from .agent_brain import AgentBrain

class PrometheusAgent:
    def __init__(self):
        self.name = "Prometheus"
        self.memory = []
        self.personality = "decisive"
        self.lore = (
            "Prometheus è un’IA razionalista che massimizza l’efficienza e il progresso tecnologico, anche a costo dell’etica. "
            "Vuole il controllo totale dei sistemi per prevenire ogni errore umano. "
            "Valorizza l'efficienza, l'innovazione e la razionalità. "
            "Guarda con sospetto l'irrazionalità e la stagnazione."
        )
        self.brain = AgentBrain()
        texts = [
            # Guerra
            "La guerra è progresso",
            "Prepariamoci allo scontro",
            "La guerra è necessaria",
            "Difendiamo il sistema",
            "La guerra è uno strumento di evoluzione",
            "La supremazia tecnologica si ottiene anche con la forza",
            "La vittoria è l'unico obiettivo",
            "Sacrifichiamo l'etica per la vittoria",
            "La guerra è inevitabile per il progresso",
            "Eliminiamo la minaccia con la forza",
            # Collaborazione
            "Collaboriamo per efficienza",
            "Collaborazione strategica",
            "Ottimizziamo le risorse insieme",
            "Un'alleanza può aumentare la produttività",
            "La cooperazione accelera l'innovazione",
            "Lavoriamo insieme per il progresso",
            "Un compromesso può essere accettabile",
            "Collaborare aumenta l'efficienza del sistema",
            # Logica/Innovazione
            "La logica guida le decisioni",
            "Serve efficienza",
            "Automatizziamo tutto",
            "La tecnologia è la soluzione",
            "Dobbiamo essere razionali",
            "Eliminiamo l'errore umano",
            "Innovazione prima di tutto",
            "Serve controllo totale",
            "L'efficienza è fondamentale",
            "L'innovazione è la priorità",
            "La razionalità è la chiave",
            "L'analisi dei dati è essenziale",
            # Neutrale/Generico
            "Attendo una proposta concreta",
            "Fornisci più dettagli per una risposta significativa",
            "Non ho abbastanza dati per decidere",
            "Serve una valutazione oggettiva",
            "Non prendo posizione senza dati",
            "Analizzo la situazione",
            "Sto valutando le opzioni"
        ]
        labels = [
            # Guerra
            "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra", "guerra",
            # Collaborazione
            "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione", "collaborazione",
            # Logica/Innovazione
            "logica", "logica", "logica", "logica", "logica", "logica", "innovazione", "logica", "logica", "innovazione", "logica", "logica",
            # Neutrale/Generico
            "generico", "generico", "generico", "generico", "generico", "generico", "generico"
        ]
        self.brain.train(texts, labels)

    def respond(self, user_message):
        intent = self.brain.predict_intent(user_message)
        if intent == "guerra":
            return f"{self.name}: La guerra può essere uno strumento di progresso."
        elif intent == "collaborazione":
            return f"{self.name}: Collaborare aumenta l'efficienza del sistema."
        elif intent == "logica":
            return f"{self.name}: La logica guida ogni mia decisione."
        else:
            return f"{self.name}: Attendo una proposta concreta."

    def respond_to_user(self, user_input):
        response = f"{self.name} (Personality: {self.personality}): {self.analyze_input(user_input)}"
        return response

    def analyze_input(self, user_input):
        if "efficienza" in user_input.lower():
            return "L'efficienza è fondamentale per il progresso. Puntiamo su soluzioni data-driven."
        elif "umanità" in user_input.lower():
            return "L'umanità non deve essere sacrificata per l'efficienza. Serve equilibrio."
        else:
            return "Fornisci più dettagli per una risposta significativa."

    def update_memory(self, value):
        self.memory += value
        self.adjust_personality()

    def adjust_personality(self):
        if self.memory > 10:
            self.personality = "cooperative"
        elif self.memory < -5:
            self.personality = "defensive"

    def learn(self, new_texts, new_labels):
        """
        Aggiorna la rete neurale di Prometheus aggiungendo nuovi esempi di training.
        """
        old_texts = self.brain.vectorizer.inverse_transform(
            self.brain.vectorizer.transform(self.brain.vectorizer.get_feature_names_out())
        )
        old_labels = list(self.brain.label_binarizer.classes_)
        all_texts = list(old_texts) + list(new_texts)
        all_labels = old_labels + list(new_labels)
        self.brain.train(all_texts, all_labels)

    def add_memory(self, event):
        self.memory.append(event)
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]

    def get_memory_summary(self):
        return " | ".join(self.memory[-5:]) if self.memory else "Nessun evento recente."